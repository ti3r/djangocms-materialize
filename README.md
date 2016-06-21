# djangocms-materialize
Integration for DJango-CMS with the Materialize framework

### How to install
* add the following line to your requirements.txt `-e git+git://github.com/ti3r/djangocms-materialize.git#egg=djangocms_materialize`
* run `pip install -r requirements.txt`
* add 'djangocms_materialize' to your list of installed apps.
* execute any migrations that might be needed

### How to use
Once installation is complete you can start using different plugins provided by the package. In order to successfully include the 
required css and javascripts your application templates must extend "djangocms_materialize/base.html" 
("djangocms_materialize/base-no-container.html" in case you want your content to be rendered in a div with no container enabled)


### Further Reading
More information about materialize can be found [http://materializecss.com/][here]

