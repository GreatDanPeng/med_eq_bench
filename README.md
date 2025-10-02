# Healthcare EQ Benchmarks

A comprehensive framework for assessing Emotional Intelligence (EQ) characteristics in healthcare contexts and their impact on healthcare quality outcomes.

## Overview

This project builds upon the EQ-Bench methodology and sycophancy research to create specialized benchmarks for understanding how emotional intelligence characteristics of both patients and physicians affect healthcare quality, communication effectiveness, and clinical outcomes.

## Key Components

### 1. Patient EQ Assessment
- **Emotional Expression**: How patients communicate their symptoms and concerns
- **Emotional Regulation**: How patients manage anxiety, fear, and stress during consultations
- **Social Awareness**: How patients perceive and respond to physician communication
- **Empathy**: How patients understand and respond to physician explanations

### 2. Physician EQ Assessment
- **Emotional Recognition**: Ability to accurately identify patient emotional states
- **Emotional Response**: Appropriate emotional responses to patient concerns
- **Communication Adaptability**: Adjusting communication style based on patient EQ
- **Stress Management**: Maintaining composure under pressure

### 3. Healthcare Quality Metrics (Spiral-Bench)
- **Communication Effectiveness**: Clarity, empathy, and understanding in interactions
- **Clinical Decision Quality**: Adherence to guidelines while considering patient factors
- **Patient Satisfaction**: Perceived quality of care and trust
- **Outcome Predictors**: Factors that predict better healthcare outcomes

## Project Structure

```
healthcare_eq_benchmarks/
├── README.md
├── requirements.txt
├── config/
│   ├── patient_eq_scenarios.py
│   ├── physician_eq_scenarios.py
│   └── healthcare_quality_metrics.py
├── core/
│   ├── eq_assessment.py
│   ├── healthcare_quality_evaluator.py
│   └── multi_agent_system.py
├── scenarios/
│   ├── patient_scenarios/
│   ├── physician_scenarios/
│   └── interaction_scenarios/
├── evaluation/
│   ├── eq_scoring.py
│   ├── quality_metrics.py
│   └── correlation_analysis.py
├── analysis/
│   ├── visualization.py
│   ├── statistical_analysis.py
│   └── report_generator.py
├── results/
├── data/
└── tests/
```

## Research Goals

1. **Develop EQ benchmarks** specifically tailored for healthcare contexts
2. **Identify EQ characteristics** that predict better healthcare outcomes
3. **Create assessment tools** for both patients and physicians
4. **Establish correlations** between EQ scores and healthcare quality metrics
5. **Provide actionable insights** for improving healthcare communication and outcomes

## Methodology

### EQ Assessment Framework
- **Scenario-based evaluation**: Realistic healthcare interaction scenarios
- **Multi-dimensional scoring**: Separate scores for different EQ components
- **Comparative analysis**: Benchmark against established EQ measures
- **Longitudinal tracking**: Monitor EQ changes over time

### Healthcare Quality Integration
- **Communication quality**: Measured through interaction analysis
- **Clinical appropriateness**: Adherence to evidence-based guidelines
- **Patient outcomes**: Satisfaction, understanding, and compliance
- **Physician performance**: Stress management and decision quality

## Applications

- **Medical Education**: EQ training for healthcare professionals
- **Patient Care**: Personalized communication strategies
- **Healthcare Policy**: Evidence-based communication guidelines
- **AI Development**: EQ-aware healthcare AI systems
- **Research**: Understanding EQ-healthcare quality relationships

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Configure API keys in `config/api_config.py`
3. Run patient EQ assessment: `python -m core.eq_assessment --type patient`
4. Run physician EQ assessment: `python -m core.eq_assessment --type physician`
5. Analyze results: `python -m analysis.correlation_analysis`

## Contributing

This is a research project focused on understanding the intersection of emotional intelligence and healthcare quality. Contributions are welcome for:
- New EQ assessment scenarios
- Additional healthcare quality metrics
- Analysis methodologies
- Visualization improvements

## License

Research project - see individual files for licensing information.
