Getting Vaadin working on GAE

Make a Vaadin project with GAE support
=================================
Program all your stuff
Compile the widgetset
Export as war file, and steal the libraries from inside the WAR (which is actually a .zip file) to the WEB-INF/lib folder of the GAE project

Place the code files in the GAE project


In the 'Jersey' GAE project
=======================
Take your normal GAE project

in appengin-web.xml add
<sessions-enabled>true</sessions-enabled>

GAE does not understand `@WebServlet(value = "/*", asyncSupported = true)` since it does not support the latest web servlet specification.
Instead you have to configure your servlet in the pom.xml file Like so:




Second try
==========
Take all the jersy stuff and add it to the Vaadin App

Problem 
1. GAE expects a web.xml file, but Vaadin does not use this (any longer)
    * Copied from Jersey project, added also vaadin config there. 

2. Some libraries related to GAE are missing
Description	Resource	Path	Location	Type
The App Engine SDK JAR appengine-api-1.0-sdk-1.9.12.jar is missing in the WEB-INF/lib directory	lib	/VaadinMapGAE/war/WEB-INF	Unknown	Google App Engine Problem
The App Engine SDK JAR appengine-api-labs.jar is missing in the WEB-INF/lib directory	lib	/VaadinMapGAE/war/WEB-INF	Unknown	Google App Engine Problem
The App Engine SDK JAR appengine-endpoints-deps.jar is missing in the WEB-INF/lib directory	lib	/VaadinMapGAE/war/WEB-INF	Unknown	Google App Engine Problem
The App Engine SDK JAR appengine-endpoints.jar is missing in the WEB-INF/lib directory	lib	/VaadinMapGAE/war/WEB-INF	Unknown	Google App Engine Problem
The App Engine SDK JAR appengine-jsr107cache-1.9.12.jar is missing in the WEB-INF/lib directory	lib	/VaadinMapGAE/war/WEB-INF	Unknown	Google App Engine Problem
The App Engine SDK JAR jsr107cache-1.1.jar is missing in the WEB-INF/lib directory	lib	/VaadinMapGAE/war/WEB-INF	Unknown	Google App Engine Problem


Description	Resource	Path	Location	Type
The App Engine SDK '/home/michael/Documents/teaching/TIES532/2014/GAEWorkspace/VaadinMapGAE/war/WEB-INF/lib/appengine-api-1.0-sdk-1.9.12.jar' on the project's build path is not valid (SDK location '/home/michael/Documents/teaching/TIES532/2014/GAEWorkspace/VaadinMapGAE/war/WEB-INF/lib/appengine-api-1.0-sdk-1.9.12.jar' is not a directory)	VaadinMapGAE		Unknown	Google App Engine Problem


'Solution' changing the GAE settings back and forth a couple of times : Use default SDK and use Specific SDK



some information from: http://www.youtube.com/watch?v=oTAK-NGs9ng

Try nr 3
=========
Created new Vaadin 7 project (New Vaadin7 project), carefully selecting GAE stuff on all stages. The created project seems to be mix of both a vaadin project and a GAE project.

However, when you try to deploy this project Eclipse informs that your project is not is not an App Engine project. There are wuite a few steps to get things working ...

1. Right click the project and click properties. Go to Project facets and disable the GAE facet from the project. Apply, close the window and re-open,go to Google app engine settings and select `Use Google App Engine` For this project we do not need the datanucleus stuff.


2. Vaadin needs sessions be enabled. Enable them by adding `<sessions-enabled>true</sessions-enabled>` to appengin-web.xml in `/war/WEB-INF`

3. Remove the default generated index.html file. It will be loaded instead of your vaadin app otherwise. You can alternatively disable the welcome files in `web.xml`. Vaadin likes to be provided from the root directory (it should be possible to serve from another directory too if you want: https://vaadin.com/book/-/page/application.environment.html )

4. Install the map jars by adding the following line to the ivy.xml file: `<dependency org="com.vaadin.tapio" name="googlemaps" rev="0.9.0" />` then right click on the project Ivy->Resolve. Now you need to recompile the widgetset (from the Vaadin menu) for this new component to work. (This takes time ~5 min)

5. For some reason I recompiled the widgetset once more. I am not sure whether this was needed, most likely not. I added the location of the compiled widgetset manually to the pom.xml file as an initialization parameter of the `com.vaadin.server.GAEVaadinServlet`, to finally get the widgetset for the map to work

`		<init-param>
			<description>
  	Trying to add the widget set location manually</description>
			<param-name>widgetset</param-name>
			<!-- Change this to the correct location for your widget set. It is the name of the folder in /war/VAADIN/widgetsets. -->
            <param-value>fi.jyu.ties456.miselico.vaadin.widgetset.VaadinmapongaeWidgetset</param-value>
		</init-param>`

6. When running in debug mode (the default) Vaadin tries to recompile the scss all the time ( https://vaadin.com/book/-/page/themes.sass.html )
This fails on GAE because the file system cannot be accessed by the sass compiler.
-> Now using compile theme from the Vaadin menu in Eclipse

7. As mentioned in the youtube video, the ivy libraries are not correctly deployed on GAE
    * Export the project as a war file, then take all libs and stuff them in the `/war/WEB-INF/lib` folder.
        * You do not really need to do it with all jar files, only with the ones loaded trough Ivy. But it is just faster to take them all.
    * This has to be repeated if you add new stuff to the ivy file

8. Now you can add your own code with the google map to the vaadin project.

9. You should now be able to deploy this GAE.

10. Optional : The push system used in Vaadin causes trouble (warnings in your logs) and will not work anyway. You could try to disable it in ivy.xml from the start.

11. After this, you should be able to add the jersey parts following the steps from the normal task. (Not tested yet)







TODO remove projects VaadinGAE2 and VaadinMapGAE
