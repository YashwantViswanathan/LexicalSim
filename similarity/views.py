from django.shortcuts import render
from .forms import SentenceForm
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(request):
    similarity_score = None
    match_words = None

    if request.method == 'POST':
        form = SentenceForm(request.POST)
        if form.is_valid():
            sentence1 = form.cleaned_data['sentence1']
            sentence2 = form.cleaned_data['sentence2']

            documents = [sentence1, sentence2]

            tfidf_vectorizer = TfidfVectorizer()
            sparse_matrix = tfidf_vectorizer.fit_transform(documents)

            doc_term_matrix = sparse_matrix.todense()

            df = pd.DataFrame(
                doc_term_matrix,
                columns=tfidf_vectorizer.get_feature_names_out(),
                index=['sentence1', 'sentence2']
            )

            similarity_score = cosine_similarity(df, df)[0, 1]
            match_keys = df.isin([0]).sum(axis=0)
            match_words = match_keys[match_keys.values == 0].keys()

    else:
        form = SentenceForm()

    return render(request, 'similarity/calculate_similarity.html', {
        'form': form,
        'similarity_score': similarity_score,
        'match_words': match_words
    })

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import SentenceSerializer

@api_view(['POST'])
def api_calculate_similarity(request):
    serializer = SentenceSerializer(data=request.data)
    if serializer.is_valid():
        sentence1 = serializer.validated_data['sentence1']
        sentence2 = serializer.validated_data['sentence2']

        documents = [sentence1, sentence2]

        tfidf_vectorizer = TfidfVectorizer()
        sparse_matrix = tfidf_vectorizer.fit_transform(documents)

        doc_term_matrix = sparse_matrix.todense()

        df = pd.DataFrame(
            doc_term_matrix,
            columns=tfidf_vectorizer.get_feature_names_out(),
            index=['sentence1', 'sentence2']
        )

        similarity_score = cosine_similarity(df, df)[0, 1]
        match_keys = df.isin([0]).sum(axis=0)
        match_words = match_keys[match_keys.values == 0].keys()

        return Response({
            'similarity_score': round(similarity_score, 2),
            'match_words': list(match_words)
        })

    return Response(serializer.errors, status=400)
