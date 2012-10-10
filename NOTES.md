
THIS FILE CONTAINS GENERAL NOTES OF THINGS TO REMEMBER, NOT DIRECTLY RELATED TO THE PROJECT.

PROJECT-RELATED STUFF IS IN:

    irb.foc.forecaster/README


Instructions for using Bazaar to publish to a web server
=================================================

Prerequirements:

 - create a group for all users

        sudo adduser --group focweb

To add a new user called john:

 - set his/her main group to focweb:

        sudo usermod -g focweb john

 - append the following command to the end of his/her ~/.bashrc file:

        umask 003

To push to the server simply push to this branch from your client machine:

        bzr+ssh://john@lis.irb.hr//home/dlucanin/projekti/lp/foc

On the server side do a:

        bzr update

(or install the push-and-update plugin as explained [here](http://wiki.bazaar.canonical.com/BazaarForWebDevs))

*Note: worth investigating [this document](http://wiki.bazaar.canonical.com/BazaarUploadForWebDev) about bzr-upload (available in the Linux repository).*

Old location, unused atm:

        bzr+ssh://john@lis.irb.hr//var/www/foc/

This is unused, as /var/www/ is stated as an unsafe location [here](https://docs.djangoproject.com/en/1.4/intro/tutorial01/) to store Django code, as it can be browsed on some web servers and publicly reveal the application's source code.

If you don't like entering your password every time, you can copy your ssh keys from the Linux client you are using for submitting changes:

        ssh-copy-id john@lis.irb.hr

Pushing from your server to the main LP repo
=============================================

To be able to code on your server you need a key there. Either copy your local ~/.ssh/id_rsa and id_rsa.pub to the server (if you trust the folks who have admin rights with your private key) or generate a new key (explained in the link below) and upload them to Launchpad by going to https://launchpad.net/~YOURUSERNAMEHERE/+editsshkeys (substitute YOURUSERNAMEHERE with... your user name).

The instructions on setting up keychain (and generating a key from scratch) can be found [here](http://www.cyberciti.biz/faq/ssh-passwordless-login-with-keychain-for-scripts/).


A quick version
---------------
Generate key

    ssh-keygen -t rsa

Upload to Launchpad by going to https://launchpad.net/~YOURUSERNAMEHERE/+editsshkeys (substitute YOURUSERNAMEHERE with... your user name) and copying the ~/.ssh/id_rsa.pub data inside the "add key" form.

Install keychain

    sudo apt-get install keychain

Add this to the end of your ~/.bashrc file

    if type keychain >/dev/null 2>/dev/null; then
      keychain --nogui -q id_rsa
      [ -f ~/.keychain/${HOSTNAME}-sh ] && . ~/.keychain/${HOSTNAME}-sh
      [ -f ~/.keychain/${HOSTNAME}-sh-gpg ] && . ~/.keychain/${HOSTNAME}-sh-gpg
    fi

Log in to your server once more or source your .bashrc file

    . .bashrc

Done.
