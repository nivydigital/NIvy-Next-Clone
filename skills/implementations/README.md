# Skill implementations (STD-01 / v2)

## Generate all 50 skills

```bash
python3 scripts/generate_std01_skills.py
python3 scripts/validate_skills_std01.py
# OK — 50 skills meet STD-01 mandatory field presence
```

Every skill file must include: objective, non_goals, inputs/outputs, 6-step procedure,
quality_checks, failure/evidence policy, dependencies, acceptance_criteria, evaluation, provenance.

Status ladder: declared → implementation → testing → active (only with unit evidence).
