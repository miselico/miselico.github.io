package bigdata.exercise1;

import java.nio.charset.StandardCharsets;
import java.util.Set;

import com.google.common.base.Preconditions;
import com.google.common.hash.HashFunction;
import com.google.common.hash.Hashing;

/**
 * An implementation of min-hashing. Logically speaking, the result of the
 * hashing is defined by the lowest index of any of the words in a permutation
 * of the universe. The universe is usually defined as the set of words which
 * are in actual use. However, it does not make any difference if we make the
 * universe larger (2^63). Many outcomes will never happen, but two outcomes
 * which are the same in a limited universe will still give the same outcomes in
 * the larger one.
 * 
 * This implementation uses a murmur3_128 hash function to 'permute' the
 * universe. Concrete, the murmur3_128 hash function works directly on the words
 * which are interpreted as indexes. The outcome of the hash function is a
 * positive long. since the output space of the murmurhash3_128 is large, and
 * the hash function of a good quality, collisions will be rather rare.
 * 
 * @author Michael Cochez
 */

public class Minhasher {

	/**
	 * The hash function which defines the permutation
	 */
	private final HashFunction hf;

	/**
	 * Create a new minhasher. The seed determines the permutation of the
	 * universe.
	 * 
	 * @param seed
	 */
	public Minhasher(int seed) {
		this.hf = Hashing.murmur3_128(seed);
	}

	/**
	 * Perform min-hash on a set of Strings.
	 * 
	 * @param doc
	 *            A set with at least one string.
	 * @return the outcome of the min-hash.
	 */
	public long hash(Set<String> doc) {
		Preconditions.checkArgument(doc.size() >= 1);
		long lowestIndex = Long.MAX_VALUE;
		for (String word : doc) {
			//in principle there is no need to take the absolute value. However, it looks a bit strange if the hash outcomes are negative numbers.
			long permutedWordIndex = Math.abs(this.hf.hashString(word, StandardCharsets.UTF_8).asLong());
			if (permutedWordIndex < lowestIndex) {
				lowestIndex = permutedWordIndex;
			}
		}
		return lowestIndex;
	}

}
