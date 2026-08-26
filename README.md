\# Enterprise Data Quality Platform



A production-oriented data quality and observability platform built on Google Cloud Platform.



\## Objectives



\- Ingest data into BigQuery

\- Validate data quality

\- Track quality metrics

\- Maintain audit history

\- Detect data issues

\- Provide reusable data-quality rules

\- Automate infrastructure with Terraform

\- Implement CI/CD with GitHub Actions



\## Architecture



```text

Data Sources

&#x20;    |

&#x20;    v

Ingestion

&#x20;    |

&#x20;    v

BigQuery

&#x20;    |

&#x20;    +------------------+

&#x20;    |                  |

&#x20;    v                  v

Data Quality        Audit / Logs

&#x20;    |

&#x20;    v

Quality Metrics

&#x20;    |

&#x20;    v

Monitoring \& Alerts

