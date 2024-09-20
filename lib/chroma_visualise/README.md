# Ally AI Chroma Visualise

## How to use


### Initialize

```python
from ally_ai_chroma.ChromaEmbeddingsVisualisation import Chroma, ChromaEmbeddingsVisualisation

chroma = Chroma()
visualise = ChromaEmbeddingsVisualisation(chroma=chroma, limit=100)
query = 'what is an ally?'
visualise(query=query)
```



