from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

documents = []
label = []

with open('Model/results.txt',"r") as f1:
    f2 = open('Model/labels.txt',"r")
    values = f1.readlines()
    labels = f2.readlines()
    data = ""
    j = 0
    for i in values:
      i = i.strip("\n")
      data += i + " "
      if (i == ""):
          documents.append(data+" ")
          data = ""
          labels[j] = labels[j].strip("\n")
          label.append(labels[j])
          j += 1
vectorizer = CountVectorizer(token_pattern=r"(?u)\b[a-zA-Z]+\b",stop_words='english', lowercase=True,min_df=2)
label_encoder = LabelEncoder()

# Fit and transform the data
X = vectorizer.fit_transform(documents)
y = label_encoder.fit_transform(label)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.17, random_state=10
)

# Initialize and fit a model
model = LogisticRegression()
model.fit(X_train, y_train)