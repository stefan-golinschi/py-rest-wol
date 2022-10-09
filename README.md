# py-rest-wol

This is a simple python application that is able to ping/suspend/poweroff/wake devices. This is useful especially in a setup where you have a workstation that needs to be started and stopped remotely.

The name of this project is inspired from @daBONDi's `go-rest-wol` repo(https://github.com/daBONDi/go-rest-wol) , which I originally used.


## Generate SSH keys

To use `py-rest-wol`, you need to generate a ssh keypair in order to authenticate with the endpoints.

```bash
ssh-keygen -C py-rest-wol -f ./id_rsa -t rsa -N "" -q
```

This will output two files
 * `id_rsa`: private key, used by `py-rest-wol` to authenticate with endpoints
 * `id_rsa.pub`: public key that needs to be registered in the `known_hosts` file on the endpoint

## How to setup a target endpoint
In order to use the remote command functionalities, like suspend/poweroff, you need to prepare it beforehand.

With security in mind, you should create an ordinary user, with limited privileges (for example, the user must have permissions to execute `systemctl suspend` as superuser). 

Also, it is recommended that the newly created user's default shell to be `rbash` instead of `bash`.

Here is a [link](https://access.redhat.com/solutions/65822) that explains how to setup `rbash` in a linux distro.

In a future release, maybe Ansible will be used to setup the remote endpoints.

```bash
cp /bin/bash /bin/rbash
useradd -s /bin/rbash woluser

echo "readonly PATH=$HOME/programs" >> ~woluser/.bash_profile
echo "export PATH" >> ~woluser/.bash_profile

mkdir ~woluser/programs
ln -s /usr/bin/sudo ~/programs/sudo
```

After this, add this line in your sudoers file using `visudo`:

```
woluser ALL=(root) NOPASSWD: /usr/bin/systemctl suspend, /usr/bin/systemctl poweroff
```

Lastly, add the public key you are using with `py-rest-wol` in endpoint's `authorized_keys` file.

```
mkdir ~woluser/.ssh
install -m 600 ~woluser/.ssh/authorized_keys
cat id_rsa.pub >> ~woluser/.ssh/authorized_keys
chown -R woluser:woluser ~woluser/
```

## Running the app

### Configuration file

The configuration file must be in yaml format.

```yml
endpoints:
  - name: workstation
    ethaddr: 1A:2B:3C:4D:5E:6F
    hostname: my-pc-hostname
    ssh_username: user
    ssh_port: 22
    enabled: true
```

|     Key       | Required |     Type      | Default value |
| ------------  | -------- | ------------- | ------------- |
| `name`        | **yes**  |   **string**  |    **N/A**    |
| `ethaddr`     | **yes**  |   **string**  |    **N/A**    | 
| `hostname`    | **yes**  |   **string**  |    **N/A**    |
| `ssh_hostname`|   no     |     string    |     root      |
| `ssh_port`    |   no     |      int      |      22       |
| `enabled`     |   no     |    boolean    |      N/A      |


### Environment variables

| Env Variable     | Default value | Description                             |
| ---------------- | ------------- | --------------------------------------- |
| `LOG_LEVEL`      |  `info`     | One of `"info"`, `"warning"`, `"debug"` |
| `LISTEN_ADDRESS` |  `0.0.0.0`    | Listen IP address                       |
| `LISTEN_PORT`    |  `8091`       | Listen TCP port                         |

### Running the app

```python
python3 py-rest-wol.py --config config.yml
```  

### Rest API

After starting the application, you will be able to control the endpoints using simple GET requests.
*  `/ping/<name>`
*  `/suspend/<name>` 
*  `/poweroff/<name>`  
*  `/wake/<name>`   

The return message is composed of a JSON object, like this:
```
{
    "method": ...,
    "status": ...,
    "message": ...
}
```

The possible return values are as follows:

| Method     | Status  | Message               |
| ---------  | ------- | --------------------- |
| `ping`     | true    | `up`                  |
|            | false   | `down`                |
|            | null    | `Endpoint not found`  |
| `suspend`  | true    | `Tried to suspend`    |
|            | false   | `down`                |
|            | null    | `Endpoint not found`  |
| `poweroff` | true    | `Tried to poweroff`   |
|            | false   | `down`                |
|            | null    | `Endpoint not found`  |
| `wake`     | true    | `Tried to wake`       |
|            | false   | `down`                |
|            | null    | `Endpoint not found`  |

## Container 

To run this application as container, you can use the container image that is published in the Packages section of this page: https://github.com/stefan-golinschi/py-rest-wol/pkgs/container/py-rest-wol

### Docker compose

Here's a simple example on how to use `py-rest-wol` container image inside a docker compose file.

```
  py-rest-wol:
    image: ghcr.io/stefan-golinschi/py-rest-wol:latest
    container_name: py-rest-wol
    environment:
      - LOG_LEVEL=info
      - LISTEN_ADDRESS=0.0.0.0
      - LISTEN_PORT=8088
    volumes:
      - configuration.yaml:/app/configuration.yaml:ro
      - ./py-rest-wol/data/ssh:/ssh:ro
    network_mode: host
    command:
      - '--config=/app/configuration.yaml'
    restart: always
```

## Home Assistant

You can use this application as a Home Assistant command_line switch. You can do this if you create a `switch` entry inside HA's `configuration.yaml` like this:

```
switch:
  - platform: command_line
    switches:
      workstation:
        command_on: 'curl -X GET http://<app hostname>:8088/wake/workstation'
        command_off: 'curl -X GET http://<app hostname>:8088/suspend/workstation'
        command_state: 'curl -X GET http://<app hostname>:8088/ping/workstation'
        value_template: '{{ value_json.message == "up" }}'

```

Just replace `app hostname` with the hostname or IP address of the `py-rest-wol` instance.
