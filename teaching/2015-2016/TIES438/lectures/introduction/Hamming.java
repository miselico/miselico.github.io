package bigdata.lecture1;

import java.util.BitSet;
import java.util.Random;

public class Hamming {
	public static void main(String[] args) {
		BitSet A = randomV(100000);
		BitSet B = randomV(100000);
		System.out.println(d_H(A, B, 100000));
		System.out.println(d_approx_H(A, B, 100000));
	}

	//We seed the random number generator to make our program easier to debug 
	private static Random r = new Random(46579864331L);

	/**
	 * Calculated the exact Hamming distance beteen the vector A and vector B
	 * @param A the first vector
	 * @param B the second vector
	 * @param len the length of the vectors
	 * @return the Hamming distance
	 */
	private static double d_H (BitSet A, BitSet B, int len){
		BitSet copyA = (BitSet) A.clone();
		copyA.xor(B); //(A xor B)_i == 1 in case A_i != B_i
		int notEqual = copyA.cardinality();//count the number of 1s
		return ((double)notEqual)/len;
	}
	
	/**
	 * Computes the average distance between the vectors by sampling 10000 positions.
	 * @param A the first vector
	 * @param B the second vector
	 * @param len the length of the vectors
	 * @return the approximate distance between the vectors
	 */
	private static double d_approx_H (BitSet A, BitSet B, int len){
		int samples = 10000;
		int equalCount = 0;
		for (int i = 0; i < samples; i++) {
			int index = r.nextInt(len);
			if (A.get(index) == B.get(index)){
				equalCount++;
			}
		}
		return 1 - ((double)equalCount)/samples;
	}
	
	/**
	 * Generates a random vector with Pr[A_i == 0] = 0.5
	 * @param len The length of the vector.
	 * @return the vector as a {@link BitSet}
	 */
	private static BitSet randomV(int len) {
		BitSet s = new BitSet();
		for (int i = 0; i < len; i++) {
			boolean value = r.nextBoolean();
			s.set(i, value);
		}
		return s;
	}

}
