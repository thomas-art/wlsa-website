from lib import *

root_dir = r"C:\uploads"
for dirpath, _, filenames in os.walk(root_dir):
    for filename in filenames:
        # 计算文件的完整路径
        file_path = os.path.join(dirpath, filename)

        # 获取新的文件名
        encoded_filename = encode_filename(filename)

        # 计算新的文件路径
        new_file_path = os.path.join(dirpath, encoded_filename)

        # 重命名文件
        os.rename(file_path, new_file_path)
        print(f"Renamed '{file_path}' to '{new_file_path}'")
