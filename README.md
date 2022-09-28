# py-rest-wol

This is a simple python application that is able to ping/suspend/poweroff/wake devices.


## Generate SSH keys

To use `py-rest-wol`, you need to generate a ssh keypair in order to authenticate with the endpoints.

```
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

```
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

Lastly, add the public key you are using with `py-rest-wol` in `authorized_keys` file.

```
mkdir ~woluser/.ssh
install -m 600 ~woluser/.ssh/authorized_keys
cat id_rsa.pub >> ~woluser/.ssh/authorized_keys
chown -R woluser:woluser ~woluser/
```
