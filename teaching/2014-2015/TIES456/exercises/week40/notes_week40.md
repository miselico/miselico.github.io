Steps

1. Create a GAE Web Application Project
2. Add the dependencies needed for Jersey
3. Add your resource classes to the project
4. Edit the pom.xml file

    <servlet>
        <servlet-name>JerseyServlet</servlet-name>
        <servlet-class>org.glassfish.jersey.servlet.ServletContainer</servlet-class>
        <init-param>
        <param-name>jersey.config.server.provider.packages</param-name>
        <param-value>fi.jyu.ties456.miselico</param-value>
        </init-param>
    </servlet>
    <servlet-mapping>
        <servlet-name>JerseyServlet</servlet-name>
        <url-pattern>/*</url-pattern>
    </servlet-mapping>

https://cloud.google.com/appengine/docs/java/tools/maven
