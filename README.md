# pypatcher
Python YAML Patcher

This simple application was created to enable devlopment automation of kubernetes microservices by patching YAML configuration files.

I thought its about time to make some contributions the opensource community that enabled me to get this far.

<b> Usage </b>
<br>
<br>
<code>
echo redis.yaml | py-patcher -p patch.yaml > redis_production.yaml
</code>

<b> Installation </b>
<br>
<br>
<code>
make install
</code>

<b> Examples </b>
<br>
<br>
This command helps communicate the current mechanics of the patch files
<br>
<br>
<code>
make example-simple
</code>
<br>
<br>
These commands demonstrate how I use pypatcher in a dev environment with makefile automation.
<br>
<br>
<code>
make example-project-dev
</code>
<br>
<code>
make example-project-prod
</code>
<br>
<br>

Pull Requests are welcome 😁