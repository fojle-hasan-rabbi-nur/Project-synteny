def read_genome_file(genome_filename):
    with open(genome_filename, 'r') as f:
        lines = f.readlines()
        seq = ''.join([line.strip() for line in lines if not line.startswith('>')])
    return seq

def read_chromosome_file(chromo_filename, genome_seq):
    chromo_list = []
    genome_length = len(genome_seq)
    with open(chromo_filename, 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:  # skip header
            parts = line.strip().split(',')
            chromo_id = parts[0]
            start = int(parts[1])
            end = int(parts[2])

            # Adjust start and end if out of bounds
            if start >= genome_length:
                chromo_seq = ""
                print(f"⚠️ Warning: Chromosome {chromo_id} start position {start} is out of genome range.")
            else:
                end = min(end, genome_length)
                chromo_seq = genome_seq[start:end]
                if chromo_seq == "":
                    print(f"⚠️ Warning: Chromosome {chromo_id} sequence is empty.")

            chromo_list.append((chromo_id, chromo_seq))
    return chromo_list

def calculate_similarity(seq1, seq2):
    if len(seq1) == 0 or len(seq2) == 0:
        return 0.0  # Return 0% if any sequence is empty

    if len(seq1) > len(seq2):
        longer = seq1
        shorter = seq2
    else:
        longer = seq2
        shorter = seq1

    max_match = 0
    for i in range(len(longer) - len(shorter) + 1):
        match_count = 0
        for j in range(len(shorter)):
            if longer[i+j] == shorter[j]:
                match_count += 1
        if match_count > max_match:
            max_match = match_count

    similarity = (max_match / len(shorter)) * 100
    return similarity

def main():
    genome_file = input("Enter genome sequence file (.fasta or .txt): ")
    chromo_file = input("Enter chromosome details file (.csv or .txt): ")

    genome_seq = read_genome_file(genome_file)
    print("✅ Genome length:", len(genome_seq))

    chromo_list = read_chromosome_file(chromo_file, genome_seq)

    best_pair = None
    best_similarity = 0

    print("\n🔬 Processing pairwise chromosome comparisons...\n")

    # Pairwise comparison between chromosomes
    for i in range(len(chromo_list)):
        for j in range(i+1, len(chromo_list)):
            id1, seq1 = chromo_list[i]
            id2, seq2 = chromo_list[j]

            similarity = calculate_similarity(seq1, seq2)
            print(f"{id1} vs {id2} similarity: {similarity:.2f}%")

            if similarity > best_similarity:
                best_similarity = similarity
                best_pair = (id1, id2)

    if best_pair:
        print("\n✔ Best Match Pair:", best_pair[0], "and", best_pair[1])
        print(f"✔ Similarity: {best_similarity:.2f}%")
    else:
        print("\n❌ No valid chromosome pairs found.")

if __name__ == "__main__":
    main()
