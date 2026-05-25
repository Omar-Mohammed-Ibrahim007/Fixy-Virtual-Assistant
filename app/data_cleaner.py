import json
import re
from timeit import main
from pdfminer.high_level import extract_text
from app.constants import INPUT_PDF, OUTPUT_JSON, Assets_dir


titles=[]
block_questions_num=[] # to get the questions associated to each header

def extract_qa(text):
    qa_pairs = []
    index=0
    counter=0

    block_questions_num= re.search(r'Document Summary\s*(.*)',text,flags=re.DOTALL) # re.DOTALL to make sure '.' captures newlines
    block_questions_num=block_questions_num.group(1) # take what inside the () after matching  pattern
    block_questions_num=re.findall(r'\b\d{1,2}(?!\.)\b',block_questions_num) # \b boundry word,(?!\.) Negative Lookahead: "Do not match if the next character is a dot"
    print("Questions Number Per Section: ",block_questions_num)


    titles= re.findall(r"\d{1,2}\.\s.*", text) # take only matching line titles of qa
    filtered_titles=[item for item in titles if '\n' not in item and int(item.split('.')[0]) <=15]
    #print('\n',filtered_titles,'\n')
    filtered_titles=filtered_titles[0:15] # to take first match
    #filtered_titles=sorted(set(filtered_titles),key=lambda x: int(x.split('.')[0])  )



    print("Titles: ",filtered_titles)

    # Split by Q and take lines of answers:
    # ex: Q305 (#12):
    blocks = re.split(r"Q\d+\s*\(#\d+\):\s*", text) # tokenize all lines begin with Q:


    for block in blocks[1:]: # take question answer pairs
        parts = re.split(r"A:", block)# split string by pattern occurance

        if len(parts) < 2:
            continue

        question = parts[0].strip().replace("\n", " ")
        question=question.split('?')[0] # to not take the right description next to headers
        answer = parts[1].strip().replace("\n", " ")

        if 'Document Summary' in answer  :  # due to miss match in last question
            answer = answer.strip().split('Document Summary')[0]

        qa_pairs.append({
            "question": question,
            "answer": answer,
            'title': filtered_titles[index],
            "section_index": index+1
        })

        counter+=1
        if counter == int(block_questions_num[index]) : # questions of title finished
            index+=1
            counter=0

    return qa_pairs


def add_metadata(qa_pairs):
    structured = []

    for id,qa in enumerate(qa_pairs,1):
        structured.append({
            "QA_ID": id,
            "question": qa["question"],
            "answer": qa["answer"],
            "context": f"Q: {qa['question']}?\nA: {qa['answer']}",
            "title": qa['title'].split('.')[1].strip(), # to remove numbers and .

            "metadata": {
                "source": "Fixy",
                "type": "faq",
                "section_index":qa['section_index'], # header number

            }
        })

    return structured



def clean(json_file):

      # 1. Load the data
      data=json_file

      # 2. Compile the regex for the form feed issue
      # re.DOTALL ensures it matches everything to the end of the string, including newlines
      form_feed_regex = re.compile(r'\f.*', flags=re.DOTALL)

      # 3. Clean the data
      for item in data:
          for key in ['answer', 'context']:
              if key in item:
                  # Strip the \f and trailing metadata
                  cleaned_text = form_feed_regex.sub('', item[key])

                  # Replace the 'ﬁ' ligature with an arrow
                  cleaned_text = cleaned_text.replace('ﬁ', '->')

                  # Optional: strip any trailing whitespace left over
                  item[key] = cleaned_text.strip()

      # 4. Save the cleaned data
      with open(f'{Assets_dir}/rag_english_data_cleaned.json', 'w', encoding='utf-8') as f:
          json.dump(data, f, indent=2, ensure_ascii=False)

      print("Data successfully cleaned and saved to 'rag_data_cleaned.json'")



def cleaner_main():
    print("[+] Extracting text from PDF...")
    text = extract_text(INPUT_PDF)


    print("[+] Extracting Q&A pairs...")
    qa_pairs = extract_qa(text)

    print(f"[+] Found {len(qa_pairs)} Q&A pairs")

    rag_data = add_metadata(qa_pairs)

    clean(rag_data)


