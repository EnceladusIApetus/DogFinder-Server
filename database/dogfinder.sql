-- phpMyAdmin SQL Dump
-- version 4.7.0
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Generation Time: May 22, 2017 at 11:51 AM
-- Server version: 8.0.1-dmr
-- PHP Version: 7.0.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dogfinder`
--

-- --------------------------------------------------------

--
-- Table structure for table `authtoken_token`
--

CREATE TABLE `authtoken_token` (
  `key` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(80) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext COLLATE utf8_unicode_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `fcm_django_fcmdevice`
--

CREATE TABLE `fcm_django_fcmdevice` (
  `id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `date_created` datetime(6) DEFAULT NULL,
  `device_id` varchar(150) COLLATE utf8_unicode_ci DEFAULT NULL,
  `registration_id` longtext COLLATE utf8_unicode_ci NOT NULL,
  `type` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `server_chat`
--

CREATE TABLE `server_chat` (
  `id` int(11) NOT NULL,
  `message` longtext COLLATE utf8_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `lost_and_found_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `server_coordinate`
--

CREATE TABLE `server_coordinate` (
  `id` int(11) NOT NULL,
  `name` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `server_dog`
--

CREATE TABLE `server_dog` (
  `id` int(11) NOT NULL,
  `name` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `breed` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `note` longtext COLLATE utf8_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `server_doglocation`
--

CREATE TABLE `server_doglocation` (
  `id` int(11) NOT NULL,
  `name` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `coordinate_id` int(11) NOT NULL,
  `dog_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `server_dogstatus`
--

CREATE TABLE `server_dogstatus` (
  `id` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `note` longtext COLLATE utf8_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `dog_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `server_file`
--

CREATE TABLE `server_file` (
  `id` int(11) NOT NULL,
  `name` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `path` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `server_image`
--

CREATE TABLE `server_image` (
  `id` int(11) NOT NULL,
  `name` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `path` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `server_instance`
--

CREATE TABLE `server_instance` (
  `id` int(11) NOT NULL,
  `raw_features` longtext COLLATE utf8_unicode_ci,
  `reduced_features` longtext COLLATE utf8_unicode_ci,
  `label` int(11) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `dog_id` int(11) NOT NULL,
  `image_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `server_locationimg`
--

CREATE TABLE `server_locationimg` (
  `id` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `image_id` int(11) NOT NULL,
  `lost_and_found_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `server_lostandfound`
--

CREATE TABLE `server_lostandfound` (
  `id` int(11) NOT NULL,
  `type` int(11) NOT NULL,
  `note` longtext COLLATE utf8_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `dog_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `server_notification`
--

CREATE TABLE `server_notification` (
  `id` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `lost_and_found_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `server_user`
--

CREATE TABLE `server_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `fb_id` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `fb_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `fb_token` longtext COLLATE utf8_unicode_ci NOT NULL,
  `fb_token_exp` datetime(6) DEFAULT NULL,
  `role` int(11) NOT NULL,
  `email` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `telephone` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `birth_date` datetime(6) DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `fb_profile_image` longtext COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD PRIMARY KEY (`key`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_server_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_de54fa62` (`expire_date`);

--
-- Indexes for table `fcm_django_fcmdevice`
--
ALTER TABLE `fcm_django_fcmdevice`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fcm_django_fcmdevice_user_id_6cdfc0a2_fk_server_user_id` (`user_id`),
  ADD KEY `fcm_django_fcmdevice_9379346c` (`device_id`);

--
-- Indexes for table `server_chat`
--
ALTER TABLE `server_chat`
  ADD PRIMARY KEY (`id`),
  ADD KEY `server_chat_user_id_5085f3fa_fk_server_user_id` (`user_id`),
  ADD KEY `server_chat_lost_and_found_id_1725f3e3_fk_server_lostandfound_id` (`lost_and_found_id`);

--
-- Indexes for table `server_coordinate`
--
ALTER TABLE `server_coordinate`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `server_dog`
--
ALTER TABLE `server_dog`
  ADD PRIMARY KEY (`id`),
  ADD KEY `server_dog_user_id_bf44cdd9_fk_server_user_id` (`user_id`);

--
-- Indexes for table `server_doglocation`
--
ALTER TABLE `server_doglocation`
  ADD PRIMARY KEY (`id`),
  ADD KEY `server_doglocatio_coordinate_id_5a970838_fk_server_coordinate_id` (`coordinate_id`),
  ADD KEY `server_doglocation_dog_id_5558d8c6_fk_server_dog_id` (`dog_id`);

--
-- Indexes for table `server_dogstatus`
--
ALTER TABLE `server_dogstatus`
  ADD PRIMARY KEY (`id`),
  ADD KEY `server_dogstatus_dog_id_b40d65cd_fk_server_dog_id` (`dog_id`);

--
-- Indexes for table `server_file`
--
ALTER TABLE `server_file`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `server_image`
--
ALTER TABLE `server_image`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `server_instance`
--
ALTER TABLE `server_instance`
  ADD PRIMARY KEY (`id`),
  ADD KEY `server_instance_dog_id_8510ee8a_fk_server_dog_id` (`dog_id`),
  ADD KEY `server_instance_image_id_012c19fc_fk_server_image_id` (`image_id`);

--
-- Indexes for table `server_locationimg`
--
ALTER TABLE `server_locationimg`
  ADD PRIMARY KEY (`id`),
  ADD KEY `server_locationimg_image_id_0e1b5bcc_fk_server_image_id` (`image_id`),
  ADD KEY `server_loca_lost_and_found_id_e6e8a25a_fk_server_lostandfound_id` (`lost_and_found_id`);

--
-- Indexes for table `server_lostandfound`
--
ALTER TABLE `server_lostandfound`
  ADD PRIMARY KEY (`id`),
  ADD KEY `server_lostandfound_dog_id_7c868830_fk_server_dog_id` (`dog_id`),
  ADD KEY `server_lostandfound_user_id_77fa9365_fk_server_user_id` (`user_id`);

--
-- Indexes for table `server_notification`
--
ALTER TABLE `server_notification`
  ADD PRIMARY KEY (`id`),
  ADD KEY `server_noti_lost_and_found_id_5f3c5f1d_fk_server_lostandfound_id` (`lost_and_found_id`),
  ADD KEY `server_notification_user_id_785eecb2_fk_server_user_id` (`user_id`);

--
-- Indexes for table `server_user`
--
ALTER TABLE `server_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `fb_id` (`fb_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;
--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;
--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;
--
-- AUTO_INCREMENT for table `fcm_django_fcmdevice`
--
ALTER TABLE `fcm_django_fcmdevice`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT for table `server_chat`
--
ALTER TABLE `server_chat`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `server_coordinate`
--
ALTER TABLE `server_coordinate`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `server_dog`
--
ALTER TABLE `server_dog`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=731;
--
-- AUTO_INCREMENT for table `server_doglocation`
--
ALTER TABLE `server_doglocation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `server_dogstatus`
--
ALTER TABLE `server_dogstatus`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `server_file`
--
ALTER TABLE `server_file`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `server_image`
--
ALTER TABLE `server_image`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1774;
--
-- AUTO_INCREMENT for table `server_instance`
--
ALTER TABLE `server_instance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=731;
--
-- AUTO_INCREMENT for table `server_locationimg`
--
ALTER TABLE `server_locationimg`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `server_lostandfound`
--
ALTER TABLE `server_lostandfound`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=728;
--
-- AUTO_INCREMENT for table `server_notification`
--
ALTER TABLE `server_notification`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `server_user`
--
ALTER TABLE `server_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD CONSTRAINT `authtoken_token_user_id_35299eff_fk_server_user_id` FOREIGN KEY (`user_id`) REFERENCES `server_user` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permissi_content_type_id_2f476e4b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_server_user_id` FOREIGN KEY (`user_id`) REFERENCES `server_user` (`id`);

--
-- Constraints for table `fcm_django_fcmdevice`
--
ALTER TABLE `fcm_django_fcmdevice`
  ADD CONSTRAINT `fcm_django_fcmdevice_user_id_6cdfc0a2_fk_server_user_id` FOREIGN KEY (`user_id`) REFERENCES `server_user` (`id`);

--
-- Constraints for table `server_chat`
--
ALTER TABLE `server_chat`
  ADD CONSTRAINT `server_chat_lost_and_found_id_1725f3e3_fk_server_lostandfound_id` FOREIGN KEY (`lost_and_found_id`) REFERENCES `server_lostandfound` (`id`),
  ADD CONSTRAINT `server_chat_user_id_5085f3fa_fk_server_user_id` FOREIGN KEY (`user_id`) REFERENCES `server_user` (`id`);

--
-- Constraints for table `server_dog`
--
ALTER TABLE `server_dog`
  ADD CONSTRAINT `server_dog_user_id_bf44cdd9_fk_server_user_id` FOREIGN KEY (`user_id`) REFERENCES `server_user` (`id`);

--
-- Constraints for table `server_doglocation`
--
ALTER TABLE `server_doglocation`
  ADD CONSTRAINT `server_doglocatio_coordinate_id_5a970838_fk_server_coordinate_id` FOREIGN KEY (`coordinate_id`) REFERENCES `server_coordinate` (`id`),
  ADD CONSTRAINT `server_doglocation_dog_id_5558d8c6_fk_server_dog_id` FOREIGN KEY (`dog_id`) REFERENCES `server_dog` (`id`);

--
-- Constraints for table `server_dogstatus`
--
ALTER TABLE `server_dogstatus`
  ADD CONSTRAINT `server_dogstatus_dog_id_b40d65cd_fk_server_dog_id` FOREIGN KEY (`dog_id`) REFERENCES `server_dog` (`id`);

--
-- Constraints for table `server_instance`
--
ALTER TABLE `server_instance`
  ADD CONSTRAINT `server_instance_dog_id_8510ee8a_fk_server_dog_id` FOREIGN KEY (`dog_id`) REFERENCES `server_dog` (`id`),
  ADD CONSTRAINT `server_instance_image_id_012c19fc_fk_server_image_id` FOREIGN KEY (`image_id`) REFERENCES `server_image` (`id`);

--
-- Constraints for table `server_locationimg`
--
ALTER TABLE `server_locationimg`
  ADD CONSTRAINT `server_loca_lost_and_found_id_e6e8a25a_fk_server_lostandfound_id` FOREIGN KEY (`lost_and_found_id`) REFERENCES `server_lostandfound` (`id`),
  ADD CONSTRAINT `server_locationimg_image_id_0e1b5bcc_fk_server_image_id` FOREIGN KEY (`image_id`) REFERENCES `server_image` (`id`);

--
-- Constraints for table `server_lostandfound`
--
ALTER TABLE `server_lostandfound`
  ADD CONSTRAINT `server_lostandfound_dog_id_7c868830_fk_server_dog_id` FOREIGN KEY (`dog_id`) REFERENCES `server_dog` (`id`),
  ADD CONSTRAINT `server_lostandfound_user_id_77fa9365_fk_server_user_id` FOREIGN KEY (`user_id`) REFERENCES `server_user` (`id`);

--
-- Constraints for table `server_notification`
--
ALTER TABLE `server_notification`
  ADD CONSTRAINT `server_noti_lost_and_found_id_5f3c5f1d_fk_server_lostandfound_id` FOREIGN KEY (`lost_and_found_id`) REFERENCES `server_lostandfound` (`id`),
  ADD CONSTRAINT `server_notification_user_id_785eecb2_fk_server_user_id` FOREIGN KEY (`user_id`) REFERENCES `server_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
