# build rds from roles
library(readxl)
library(tidyverse)
library(snakecase)

# -----------------------------------------------------------------------------
# 1. Read
# -----------------------------------------------------------------------------

raw <- read_excel("./ci_rwaa_org_v2/20260407_rwaa_sa_roles_cleaned.xlsx")

roles <- raw |>
  
  mutate(name = to_snake_case(name))

# -----------------------------------------------------------------------------
# 2. Rename columns to short keys
# -----------------------------------------------------------------------------

#keeping format from expert 
roles_standard <- roles |>
  saveRDS("./ci_rwaa_org_v2/dat_rwaa_sa_roles.rds")

# View(roles)
