import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Iterator;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Main {

	public static void main(String[] args) throws Exception {

		BufferedReader r;
		String l;

		String patterns = "C:\\Users\\mtb\\Desktop\\IRWM\\SummerSchool\\IE-Challenge\\PATTY\\yago-relation-paraphrases.txt";
		String articles = "C:\\Users\\mtb\\Desktop\\IRWM\\SummerSchool\\IE-Challenge\\Wiki-scientists\\scientists-LINKS.txt";

		String last = null, next = null, prefix = null, suffix, key;

		HashMap<String, String> map = new HashMap<String, String>(50000);

		// buffered file reader, reads the patterns file line by line
		r = new BufferedReader(new FileReader(patterns));
		while ((l = r.readLine()) != null) {
			String[] values = l.split("\t");
			// just remove all POS tags for now and trim the patterns
			values[1] = values[1].replaceAll("\\[\\[.*?\\]\\]", "");
			values[1] = values[1].substring(0, values[1].length() - 1).trim();
			if (values[1].indexOf(' ') > -1)
				map.put(values[1], values[0]);
		}
		r.close();

		// regex pattern matcher for Wiki links
		Pattern p = Pattern.compile("\\[\\[.*?\\]\\]");

		// buffered file reader, reads the articles file line by line
		r = new BufferedReader(new InputStreamReader(new FileInputStream(
				articles), "UTF8"));

		int c = 0;
		while ((l = r.readLine()) != null) {

			// System.out.println(l.length() + "\t" + l);

			if (l.startsWith("====PAGE-START===="))
				continue;

			Matcher m = p.matcher(l);

			int s = -1, e = -1, t = -1;
			while (m.find()) {

				prefix = l.substring(Math.max(0, e), m.start());
				if ((t = l.indexOf("[[", m.end())) > -1)
					suffix = l.substring(m.end(), Math.min(t, l.length()));
				else
					suffix = l.substring(m.end(), l.length());

				// extract the next entity candidate
				s = m.start();
				e = m.end();
				next = l.substring(s, e);
				if ((t = next.indexOf("|")) > -1)
					next = next.substring(0, t) + "]]";

				// heuristically check for pairs of links not separated by '.'
				if (last != null && prefix.indexOf('.') < 0) {

					// find candidates for matching YAGO2 relations
					for (Iterator<String> i = map.keySet().iterator(); i
							.hasNext();) {
						key = i.next();
						if (prefix.indexOf(key) > -1) {
							System.out.println(c + " \t " + key + " -> "
									+ map.get(key) + " \t " + last + " \t "
									+ prefix + "\t" + next + "\t" + suffix);
							c++;
						}
					}
				}
				last = next;
			}
			last = null;
		}
		r.close();
	}
}
