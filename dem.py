import os

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

def calculate_alignment(seq1, seq2):
    if len(seq1) == 0 or len(seq2) == 0:
        return 0.0, []

    max_match = 0
    best_alignment = []

    for offset in range(-len(seq2)+1, len(seq1)):
        match_count = 0
        alignment_line = ""

        for i in range(len(seq2)):
            pos_in_seq1 = i + offset
            if 0 <= pos_in_seq1 < len(seq1):
                if seq1[pos_in_seq1] == seq2[i]:
                    alignment_line += "R"
                    match_count += 1
                else:
                    alignment_line += "W"
            else:
                alignment_line += "X"

        similarity = (match_count / len(seq2)) * 100

        visual_top = seq1
        visual_mid = (" " * max(0, offset)) + alignment_line
        visual_bottom = (" " * max(0, offset)) + seq2

        if match_count > max_match:
            max_match = match_count
            best_alignment = [visual_top, visual_mid, visual_bottom, f"Similarity: {similarity:.2f}%"]

    final_similarity = (max_match / len(seq2)) * 100
    return final_similarity, best_alignment

def main():
    genome_file = input("Enter genome sequence file (.fasta or .txt): ")
    chromo_file = input("Enter chromosome details file (.csv or .txt): ")

    # ✅ File existence check
    if not os.path.exists(genome_file):
        print(f"❌ Error: File '{genome_file}' not found.")
        return
    if not os.path.exists(chromo_file):
        print(f"❌ Error: File '{chromo_file}' not found.")
        return

    genome_seq = read_genome_file(genome_file)
    print("✅ Genome length:", len(genome_seq))

    chromo_list = read_chromosome_file(chromo_file, genome_seq)

    best_pair = None
    best_similarity = 0
    best_alignment_result = []

    print("\n🔬 Processing pairwise chromosome comparisons...\n")

    for i in range(len(chromo_list)):
        for j in range(i+1, len(chromo_list)):
            id1, seq1 = chromo_list[i]
            id2, seq2 = chromo_list[j]

            similarity, alignment_visual = calculate_alignment(seq1, seq2)

            print(f"\n{id1} vs {id2} similarity: {similarity:.2f}%")
            for line in alignment_visual:
                print(line)

            if similarity > best_similarity:
                best_similarity = similarity
                best_pair = (id1, id2)
                best_alignment_result = alignment_visual

    if best_pair:
        print("\n✔ Best Match Pair:", best_pair[0], "and", best_pair[1])
        print(f"✔ Highest Similarity: {best_similarity:.2f}%")
        print("✔ Best Alignment:")
        for line in best_alignment_result:
            print(line)
    else:
        print("\n❌ No valid chromosome pairs found.")

if __name__ == "__main__":
    main()
