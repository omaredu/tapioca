import pandas as pd
class PostingFile:
    def __init__(self, posting_path):
        self.posting_path = posting_path
        self.posting_df = pd.read_csv(posting_path)
    def get_documents(self, position):
        if 0 <= position < len(self.posting_df):
            return self.posting_df.iloc[position].to_dict()
        return None
    def save_posting_file(self, output_path):
        self.posting_df.to_csv(output_path, index=False)
    def insert_entry(self, file_name, frequency):
        new_entry = {"Archivo": file_name, "Repeticiones en el archivo": frequency}
        self.posting_df = self.posting_df.append(new_entry, ignore_index=True)
        self.save_posting_file(self.posting_path)
if __name__ == "__main__":
    posting = PostingFile("out/posting.csv")
    print(posting.get_documents(0))
