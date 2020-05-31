package fi.jyu.ties532.advanced.bustravel.client;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;

import org.xerial.snappy.SnappyInputStream;

import com.google.common.io.ByteStreams;

import de.jarnbjo.jsnappy.Buffer;
import de.jarnbjo.jsnappy.SnappyDecompressor;
import fi.jyu.ties532.advanced.bustravel.LocationProt;
import fi.jyu.ties532.advanced.bustravel.LocationProt.Response;

/**
 * This example client uses {@link SnappyInputStream} and
 * {@link SnappyDecompressor} to read the snappy data. {@link SnappyInputStream}
 * is able to convert the stream directly, but does not work on GAE.
 * {@link SnappyDecompressor} first reads the blob in memory and converts. Then
 * it is possible to read from the converted version. This works on GAE.
 * 
 * This code depends on <a href="http://code.google.com/p/jsnappy/">JSnappy</a>
 * and <a href="https://github.com/xerial/snappy-java">Snappy-Java</a> for
 * Snappy and on <a href="http://code.google.com/p/guava-libraries/">Guava</a>
 * for reading an {@link InputStream} in a byte array.
 * 
 * The {@link LocationProt} class must be compiled from the protocol buffer
 * file.
 * 
 * @author Michael Cochez
 * 
 */
public class Client {
	public static void main(String[] args) throws IOException {
		using_de_jarnbjo_jsnappy();
		using_org_xerial_snappy();
	}

	public static void using_org_xerial_snappy() throws IOException {
		InputStream input = new URL(
				"http://jyulocation.appspot.com/locate/Ag%20Alfa").openStream();
		SnappyInputStream snappy = new SnappyInputStream(input);
		Response resp = LocationProt.Response.parseFrom(snappy);
		System.out.println(resp.getStatus());
		System.out.println(resp);
	}

	public static void using_de_jarnbjo_jsnappy() throws IOException {
		InputStream input = new URL(
				"http://jyulocation.appspot.com/locate/Ag%20Alfa").openStream();
		byte[] compressedResponse = ByteStreams.toByteArray(input);
		Buffer buffer = SnappyDecompressor.decompress(compressedResponse);
		Response resp = LocationProt.Response.parseFrom(buffer.getData());
		System.out.println(resp.getStatus());
		System.out.println(resp);
	}
}
