library(dplyr)

dat_expert <- readRDS("./ci_rwaa_org_v2/dat_rwaa_sa_expert_completed.rds")
dat_roles  <- readRDS("./ci_rwaa_org_v2/dat_rwaa_sa_roles.rds")

dat_rwaa_sa_team <- dat_roles |>
  full_join(dat_expert, by = "name")

View(dat_rwaa_sa_team)

saveRDS(dat_rwaa_sa_team, "./ci_rwaa_org_v2/dat_rwaa_sa_team.rds")

write.csv(dat_rwaa_sa_team, "./ci_rwaa_org_v2/dat_rwaa_sa_team.xlsx")