# Master_Thesis
Ontology-based Text Mining in the Computational Materials Science Domain

## Step1.Collect Data
1. Extract keywords and phrases from the MAPI documentation.
run python3 MAPI_keywords_extraction.py
2. Choose suitable keywords or phrases which contains relevant articles. Then the keywords and phrases can be used to extract articles from the first journal database.
run python3 main.py
3. Thses articles have their own keywords. Repeat the second step.
run python3 repeat_extraction.py
4. Repeat the third step. But there is no new article. So the final number of the article is 9551.
5. As for the second journal database. Those artices do not have keywords. So all relevant articles in that database should be extracted. The number is 344.
run article_extraction_npj.py

## Step2.Text Mining
