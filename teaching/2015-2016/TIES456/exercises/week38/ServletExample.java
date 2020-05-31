package fi.jyu.miselico.ties456.week38.webapp_jetty;

import java.io.IOException;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet example
 */
public class ServletExample extends HttpServlet {

	/**
	 * A servlet MUST have a public no argument constructor
	 */
	public ServletExample() {
		super();
	}
	
	// Implement doGet to answer the GET method, doPost to answer the POST method
	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
		//get the paremeters from req
		String name = req.getParameter("name");
		//write the response to resp
		resp.getWriter().write("Hello " + name);
	}

}

