CREATE TABLE `daily_data`
(
  `id` int PRIMARY KEY,
  `patient_id` int,
  `water` int,
  `weight` int,
  `pulse` int,
  `temperature` int,
  `calories` int,
  `day` date
);

