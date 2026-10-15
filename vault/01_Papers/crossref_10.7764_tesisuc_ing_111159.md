---
title: "Low-rank quadratic sparse autoencoders improve LLM feature reconstruction and interpretability"
authors:
  - "Josué Cristián Tapia San Martín"
url: "https://doi.org/10.7764/tesisuc/ing/111159"
published: "2026-8-20"
citations: "0"
source: "Crossref"
id: "crossref:10.7764/tesisuc/ing/111159"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "sparse-autoencoders-interpretability"
---
# Low-rank quadratic sparse autoencoders improve LLM feature reconstruction and interpretability

**Authors**: Josué Cristián Tapia San Martín
**Published**: 2026-8-20 | **Citations**: 0 | **Source**: Crossref
**URL**: https://doi.org/10.7764/tesisuc/ing/111159

## Executive Summary & Abstract
Los sparse autoencoders (SAE) se utilizan ampliamente para descomponer las activaciones de los modelos de lenguaje en características escasas e interpretables. Sin embargo, los SAE lineales imponen fuertes restricciones geométricas a las representaciones que pueden recuperar, pese a la creciente evidencia de que muchas características en los LLM exhiben estructura de variedad intrínseca y nociones de distancia específicas que no se comportan como direcciones lineales simples. Presentamos un low-rank quadratic sparse autoencoder (LRQ-SAE) que amplía el codificador y decodificador lineales estandar con términos cuadráticos factorizados, permitiendo que cada característica latente capture interacciones de segundo orden de manera controlada mientras mantiene la escasez. Utilizando activaciones de la corriente residual de capas intermedias, observamos que los LRQ-SAE obtienen de forma consistente menor error de reconstrucción normalizado que los SAE lineales bajo igual dimensionalidad y nivel de dispersión. Para evaluar la interpretabilidad, empleamos un protocolo robusto en el que un LLM mayor infiere una definición en lenguaje natural para cada característica a partir de ejemplos de activación y luego genera nuevas frases candidatas, cuyas activaciones se utilizan para estimar la generalización a nivel de característica. Los LRQ-SAE obtienen puntuaciones de interpretabilidad sustancialmente más altas bajo esta métrica, lo que indica que la estructura cuadrática de bajo rango ayuda a recuperar características mas coherentes semánticamente y activadas de manera más fiable. Estos resultados sugieren que introducir una capacidad estructurada de segundo orden relaja las restricciones geométricas inherentes a los SAE lineales y desplaza la frontera empírica entre reconstrucción e interpretabilidad.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
Los sparse autoencoders (SAE) se utilizan ampliamente para descomponer las activaciones de los modelos de lenguaje en características escasas e interpretables. Sin embargo, los SAE lineales imponen fuertes restricciones geométricas a las representaciones que pueden recuperar, pese a la creciente evidencia de que muchas características en los LLM exhiben estructura de variedad intrínseca y nociones de distancia específicas que no se comportan como direcciones lineales simples. Presentamos un low-rank quadratic sparse autoencoder (LRQ-SAE) que amplía el codificador y decodificador lineales estandar con términos cuadráticos factorizados, permitiendo que cada característica latente capture interacciones de segundo orden de manera controlada mientras mantiene la escasez. Utilizando activaciones de la corriente residual de capas intermedias, observamos que los LRQ-SAE obtienen de forma consistente menor error de reconstrucción normalizado que los SAE lineales bajo igual dimensionalidad y nivel de dispersión. Para evaluar la interpretabilidad, empleamos un protocolo robusto en el que un LLM mayor infiere una definición en lenguaje natural para cada característica a partir de ejemplos de activación y luego genera nuevas frases candidatas, cuyas activaciones se utilizan para estimar la generalización a nivel de característica. Los LRQ-SAE obtienen puntuaciones de interpretabilidad sustancialmente más altas bajo esta métrica, lo que indica que la estructura cuadrática de bajo rango ayu
