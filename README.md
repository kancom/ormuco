Please create a small web application to demonstrate your devops skills.

Its root URL "/" should display a form that accepts three fields as input: "Name", "Favorite Color", "Cats or Dogs". This form should save the result in a relational database and ensure that "Name" is unique. You can use any technology for this (eg, it could be node.js and sqlite, or python and mysql, or golang and postgres - we don't care, but we may ask you about it).

After you have built this sample application, create an Ansible playbook to deploy it on a cloud. Yes, Ansible; please don't use chef or puppet - we're opinionated about this. If you don't have an account, don't worry - you can sign up with AWS for free and test your application on a "tiny" instance at no charge.

Bonus points if the application can be easily scaled beyond a single server. More bonus points if the server is well secured (HTTPS, firewalls, etc).

Finally, provide us with the IP address or hostname of the operational site, a copy of the application code and the Ansible playbooks necessary to deploy it, and a small document that will allow us to test it out ourselves. Add the following SSH public key, so that we can access the instance to look at your work.


http://paste.openstack.org/raw/osn4Yi7NFIb6PsYpRkT8/
