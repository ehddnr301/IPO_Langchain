import os

def write_txt(contents, file_name):
    if not os.path.exists("./IpoStatics"):
        os.makedirs("./IpoStatics")
        
    try:
        with open(f"./IpoStatics/{file_name}.txt", "w", encoding="utf-8") as f:
            f.write("\n\n\n".join(contents))
        return "Success"
    except:
        return "Fail"
