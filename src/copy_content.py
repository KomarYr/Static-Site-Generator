import os
import shutil




def copy_content(src: str, dst: str, cleaned: bool = False) -> None:
    if not cleaned:
        if os.path.exists(dst): # for first time 
            shutil.rmtree(dst)
        cleaned = True
    if not os.path.exists(dst):
        os.mkdir(dst)
    #print(f"dst created, here content: {os.listdir(dst)}")

    src_content = os.listdir(src)
    for item in src_content:
        src_path = os.path.join(src, item)
        
        if os.path.isfile(src_path):
            #print(f"this is a file: {src_path}")
            shutil.copy(src_path, dst)
        else:
            #print(f"this is folder in {src}: {src_path}")
            copy_content(src_path, os.path.join(dst, item), cleaned)
                


if __name__ == "__main__":
    print(copy_content(".."))

