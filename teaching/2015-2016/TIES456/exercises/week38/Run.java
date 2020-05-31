package fi.jyu.miselico.ties456.week38.webapp_jetty;

import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.servlet.ServletHandler;

/**
 * A basic example on how to run servlets using embedded Jetty
 *
 */
public class Run {
	public static void main(String[] args) throws Exception {
		
		ServletHandler handler = new ServletHandler();
		//add all servlets you want to use to the handler, the second argument is the path
        handler.addServletWithMapping(CreateCourse.class, "/create");
        // make the SearchTeacher Servlet accessible from http://localhost:8080/search
        handler.addServletWithMapping(SearchTeacher.class, "/search");

        //Create a new Server, add the handler to it and start
        Server server = new Server(8080);		
		server.setHandler(handler);
		server.start();
		//this dumps a lot of debug output to the console. 
		server.dumpStdErr();
		server.join();
	}
}
