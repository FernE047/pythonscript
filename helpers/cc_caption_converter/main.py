def main() -> None:
    with open("input.txt", "r") as caption_txt, open("output.str", "w") as caption_str:
        line = ""
        character = "a"
        line_index = 1
        while character:
            character = caption_txt.read(1)
            if character != "\n":
                line += character
                continue
            if not line:
                caption_str.write("\n")
                line = ""
                continue
            if line[0] != "0":
                caption_str.write(f"{line}\n")
                line = ""
                continue
            # comma = line.find(",")
            modified_line = list(line)
            modified_line[9] = "."
            modified_line[23] = "."
            line = "".join(modified_line)
            text_start = line[:13]  #:comma]
            final_text = line[14:]  # comma+1:]
            start_time = text_start[:2] + text_start[3:6] + text_start[7:]
            end_time = final_text[:2] + final_text[3:6] + final_text[7:]
            caption_str.write(f"{line_index}\n")
            caption_str.write(f"{start_time} --> {end_time}\n")
            line_index += 1
        caption_str.write(line)


if __name__ == "__main__":
    main()
