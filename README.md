# How Do You Feel? Information Retrieval in Psychotherapy and Fair Ranking Assessment

In the folder "notebooks," there are two Jupyter notebooks:

- **MatchZoo**: to run the experiments with the models provided by the Python library MatchZoo
- **BERT**: it uses TFR-BERT following the tutorial of TensorFlow. The execution requires more than 24 GiB GPU, tested on a machine with 48 GiB GPU and 45 GiB RAM.

### Publication (Conference ECIR - BIAS) 
#### Data Augmentation for Reliability and Fairness in Counselling Quality Classification 
URL: https://link.springer.com/chapter/10.1007/978-3-031-37249-0_10

Cite as (BibTex): 
```bash
@InProceedings{10.1007/978-3-031-37249-0_10,
author="Kumar, Vivek
and Medda, Giacomo
and Recupero, Diego Reforgiato
and Riboni, Daniele
and Helaoui, Rim
and Fenu, Gianni",
editor="Boratto, Ludovico
and Faralli, Stefano
and Marras, Mirko
and Stilo, Giovanni",
title="How Do You Feel? Information Retrieval in Psychotherapy and Fair Ranking Assessment",
booktitle="Advances in Bias and Fairness in Information Retrieval",
year="2023",
publisher="Springer Nature Switzerland",
address="Cham",
pages="119--133",
abstract="The recent pandemic Coronavirus Disease 2019 (COVID-19) led to an unexpectedly imposed social isolation, causing an enormous disruption of daily routines for the global community and posing a potential risk to the mental well-being of individuals. However, resources for supporting people with mental health issues remain extremely limited, raising the matter of providing trustworthy and relevant psychotherapeutic content publicly available. To bridge this gap, this paper investigates the application of information retrieval in the mental health domain to automatically filter therapeutical content by estimated quality. We have used AnnoMI, an expert annotated counseling dataset composed of high- and low-quality Motivational Interviewing therapy sessions. First, we applied state-of-the-art information retrieval models to evaluate their applicability in the psychological domain for ranking therapy sessions by estimated quality. Then, given the sensitive psychological information associated with each therapy session, we analyzed the potential risk of unfair outcomes across therapy topics, i.e., mental issues, under a common fairness definition. Our experimental results show that the employed ranking models are reliable for systematically ranking high-quality content above low-quality one, while unfair outcomes across topics are model-dependent and associated low-quality content distribution. Our findings provide preliminary insights for applying information retrieval in the psychological domain, laying the foundations for incorporating publicly available high-quality resources to support mental health. Source code available at https://github.com/jackmedda/BIAS-FairAnnoMI.",
isbn="978-3-031-37249-0"
}
```
