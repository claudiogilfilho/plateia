# Contrato de saída

## Relatório legível

1. Diagnóstico em uma frase.
2. Cobertura e limitações.
3. Classificação multiaxial e confiança.
4. Grupo comparável e confiança do benchmark.
5. Notas dos oito critérios, omitindo os não avaliados.
6. Reação provável de cada uma das cinco lentes, objeção central e ação provável.
7. Pontos fortes e riscos.
8. Exatamente três melhorias prioritárias, específicas e executáveis.
9. O que não pode ser concluído.
10. Se for referência de treinamento: aprendizados replicáveis, contingentes, não recomendáveis e hipóteses.

## JSON mínimo

```json
{
  "protocolVersion": "2.1",
  "coverage": {
    "level": "complete|partial|insufficient",
    "accessible": [],
    "missing": [],
    "limitations": []
  },
  "classification": {
    "materialFormat": "",
    "presentationFormats": [],
    "primaryFamily": "",
    "secondaryFamilies": [],
    "objectives": [],
    "segment": "",
    "subsegment": "",
    "probableAudience": "",
    "awarenessStage": "",
    "productionLevel": "simple|intermediate|complex|unknown",
    "durationBand": "",
    "pace": "",
    "mechanisms": [],
    "confidence": "low|medium|high",
    "evidence": [],
    "alternativeClassifications": [],
    "missingInformation": [],
    "needsHumanReview": false
  },
  "comparison": {
    "level": 4,
    "confidence": "low",
    "referenceIds": []
  },
  "scores": {
    "gancho": { "assessed": true, "score": 0, "justification": "", "evidence": "", "confidence": "low" },
    "clareza": { "assessed": true, "score": 0, "justification": "", "evidence": "", "confidence": "low" },
    "relevancia": { "assessed": true, "score": 0, "justification": "", "evidence": "", "confidence": "low" },
    "desejo": { "assessed": true, "score": 0, "justification": "", "evidence": "", "confidence": "low" },
    "confianca": { "assessed": true, "score": 0, "justification": "", "evidence": "", "confidence": "low" },
    "retencao": { "assessed": true, "score": 0, "justification": "", "evidence": "", "confidence": "low" },
    "acao": { "assessed": true, "score": 0, "justification": "", "evidence": "", "confidence": "low" },
    "objecoes": { "assessed": true, "score": 0, "justification": "", "evidence": "", "confidence": "low" }
  },
  "consumers": [
    { "name": "O Apressado", "overallScore": 0, "reaction": "", "mainObjection": "", "probableAction": "", "confidence": "low" }
  ],
  "synthesis": {
    "overallScore": 0,
    "divergence": 0,
    "strengths": [],
    "risks": [],
    "recommendations": ["", "", ""]
  },
  "cannotConclude": [],
  "training": {
    "replicable": [],
    "contingent": [],
    "notRecommended": [],
    "hypotheses": []
  }
}
```

O array `consumers` deve conter exatamente as cinco lentes. `recommendations` deve conter exatamente três itens.
