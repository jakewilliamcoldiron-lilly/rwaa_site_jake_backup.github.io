# build rds from expertise survey
library(readxl)
library(tidyverse)
library(snakecase)

# -----------------------------------------------------------------------------
# 1. Read
# -----------------------------------------------------------------------------

raw <- read_excel("./ci_rwaa_org_v2/20260407_rwaa_sa_expert_cleaned.xlsx")

team <- raw |>
  
  rename_with(~ to_snake_case(str_squish(.))) |>
  
  rename(
    name         = sa_name,
    optum        = optum_market_clarity_optum_cdm,
    welldoc      = well_doc_tempo_pen_data_cmh_specific,
    meps         = meps_medical_expenditure_panel_survey,
    nhanes       = nhanes_public_survey_data,
    cprd         = cprd_aurum,
    other        = other_specify_please
  ) %>% 
  
  mutate(name = to_snake_case(str_squish(name)))

# -----------------------------------------------------------------------------
# 2. Rename columns to short keys
# -----------------------------------------------------------------------------

team_completed <- team |>
  select(-other) %>% 
  filter(!is.na(optum)) %>% 
  mutate(across(everything(), ~ replace_na(., 1))) %>% 
  saveRDS("./ci_rwaa_org_v2/dat_rwaa_sa_expert_completed.rds")
# View(team_standard)

team_all <- team |>
  select(-other) %>% 
  saveRDS("./ci_rwaa_org_v2/dat_rwaa_sa_expert_all.rds")
# View(team_all)

# MUST DIFF BETWEEN COMPLETED AND ALL
# Because some people filled out survey but only put 1's for some, but not all, columns.
# Rhis means we must mutate these NAs into 1s for those that completed survey/
# However, if we do that blindly, those who didn't complete the survey will all be 1.
# Thus, drop those that are missing, and replace NAs with 1s for those that answered survey.
# When we merge with roles, must do a FULL JOIN with "expert_completed" and roles to ensure those who didn't complete
# are still on the org chart. 

team_missing_verify <- team |>
  filter(is.na(optum))
# View(team_missing_verify)
  
team_missing <- team_missing_verify %>% 
  select(name) %>% 
  saveRDS("./ci_rwaa_org_v2/dat_rwaa_sa_expert_missing.rds")
# View(team_missing) 

team_other <- team |>
  select(name, other) %>% 
  filter(!is.na(other)) %>% 
  saveRDS("./ci_rwaa_org_v2/dat_rwaa_sa_expert_other.rds") 
# View(team_other)