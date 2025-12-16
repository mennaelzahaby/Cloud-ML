FROM continuumio/miniconda3

WORKDIR /app

COPY . .

# تثبيت joblib فقط (scikit-learn موجودة بالفعل في conda)
RUN conda install scikit-learn --yes && pip install joblib

CMD ["python", "train.py"]
