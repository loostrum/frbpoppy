"""Short example of how frbpoppy works."""
from frbpoppy import CosmicPopulation, Survey, SurveyPopulation, plot

PLOT = True

# Generate an FRB population
cosmic_pop = CosmicPopulation(10000, days=3, name='example')

# Setup a survey
survey = Survey('HTRU')

# Observe the FRB population
survey_pop = SurveyPopulation(cosmic_pop, survey)

# Check the detection rates
print(survey_pop.rates())

# Plot populations
if PLOT:
    plot(cosmic_pop, survey_pop, frbcat='HTRU')
