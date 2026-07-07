---
type: reference
aliases: []
tags:
  - literature
  - research
title: "{{title}}"
authors: "{{authors}}"
year: {{date | format("YYYY")}}
journal: "{{publicationTitle}}"
doi: "{{doi}}"
read: false
related: []
---

# {{title}}

> **Authors:** {{authors}}
> **Year:** {{date | format("YYYY")}}
> **Journal:** {{publicationTitle}}
> **Links:** {{pdfZoteroLink}} | [DOI](https://doi.org/{{doi}})

---


## 📝 Abstract

> {{abstractNote}}


## 🎯 TL;DR / Core Claim
*(Write a 1-2 sentence summary of what this paper actually achieves or claims, in your own words. Why does this matter for your thesis?)*

## 🧠 Synthesis & Thoughts
*(This is where you synthesize how this relates to your work. Does it support your methodology? Does it contradict a previous paper?)*

- **Relevance**:: 
- **Methodology**:: 
- **Key Findings**::  



---

### Notes
{% for annotation in annotations -%}{%- if annotation.annotatedText -%}{% if 'Red' in annotation.colorCategory %} 
##### {{annotation.annotatedText | escape }}{% else %}
<mark class="customZot-{% if annotation.color %}{{annotation.colorCategory}} {% endif %}">{{annotation.annotatedText | escape }}</mark> ([{{annotation.page}}](zotero://open-pdf/library/items/{{annotation.attachment.itemKey}}?page={{annotation.page}}&annotation={{annotation.id}}))

{% endif %}{%- endif %} {% if annotation.imageRelativePath %} ![[{{annotation.imageRelativePath}}]]{% endif %}{% if annotation.comment %} 
>{{annotation.comment}}
{% endif %}{% endfor -%}
