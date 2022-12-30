-- phpMyAdmin SQL Dump
-- version 4.7.9
-- https://www.phpmyadmin.net/
--
-- Φιλοξενητής: localhost
-- Χρόνος δημιουργίας: 09 Νοε 2022 στις 10:38:30
-- Έκδοση διακομιστή: 5.7.30-0ubuntu0.16.04.1
-- Έκδοση PHP: 7.0.33-0ubuntu0.16.04.15

-- SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
-- SET AUTOCOMMIT = 0;
-- START TRANSACTION;
-- SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Βάση δεδομένων: `diamantop_ncRNAs4`
--

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `Function_descriptions`
--

-- CREATE DATABASE DBNAME;
-- USE DBNAME;


CREATE TABLE IF NOT EXISTS `Function_descriptions` (
  `Function_ID` int(11) NOT NULL,
  `Function_description` text,
  PRIMARY KEY (`Function_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `Genes`
--

CREATE TABLE IF NOT EXISTS `Genes` (
  `gene_stable_id` varchar(50) NOT NULL,
  `gene_description` varchar(255) DEFAULT NULL,
  `chromosome/scaffold` varchar(255) DEFAULT NULL,
  `gene_end` int(11) DEFAULT NULL,
  `gene_start` int(11) DEFAULT NULL,
  `gene_name` varchar(255) DEFAULT NULL,
  `hgnc_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`gene_stable_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `Gene_Protein`
--

CREATE TABLE IF NOT EXISTS `Gene_Protein` (
  `gene_stable_id` varchar(50) NOT NULL,
  `protein_uniprot_entry` varchar(50) NOT NULL,
  PRIMARY KEY (`gene_stable_id`,`protein_uniprot_entry`),
  KEY `fk_Gene_Protein__protein` (`protein_uniprot_entry`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `miRNAs_mature`
--

CREATE TABLE IF NOT EXISTS `miRNAs_mature` (
  `miRNAmat_id` int(11) NOT NULL AUTO_INCREMENT,
  `mature_accession` varchar(50) DEFAULT NULL,
  `mature_id` varchar(50) DEFAULT NULL,
  `mature_sequence` varchar(50) NOT NULL,
  `evidence` varchar(255) DEFAULT NULL,
  `experiment` varchar(255) DEFAULT NULL,
  `similarity` varchar(255) DEFAULT NULL,
  `sequenceid` int(11) DEFAULT NULL,
  `stemid` int(11) DEFAULT NULL,
  PRIMARY KEY (`miRNAmat_id`),
  -- KEY `fk_miRNAs_mature_sequence` (`mature_sequence`),
  KEY `fk_mature_stem` (`stemid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `miRNAs_stem`
--

CREATE TABLE IF NOT EXISTS `miRNAs_stem` (
  `miRNAstem_id` int(11) NOT NULL AUTO_INCREMENT,
  `stem_accession` varchar(50) NOT NULL,
  `stem_id` varchar(50) NOT NULL,
  `description` varchar(255) NOT NULL,
  `cc` text,
  `seq_description` varchar(255) NOT NULL,
  `sequence` text NOT NULL,
  `sequenceid` int(11) DEFAULT NULL,
  PRIMARY KEY (`miRNAstem_id`),
  KEY `fk_miRNAs_stem_sequence` (`sequenceid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `Proteins`
--

CREATE TABLE IF NOT EXISTS `Proteins` (
  `uniprot_entry` varchar(10) NOT NULL,
  `entry_name` varchar(11) DEFAULT NULL,
  `protein_name` text,
  `organism` varchar(50) DEFAULT NULL,
  `aminoacid_sequence` text,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`uniprot_entry`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `Protein_Function`
--

CREATE TABLE IF NOT EXISTS `Protein_Function` (
  `uniprot_entry` varchar(10) NOT NULL,
  `Function_ID` int(11) NOT NULL,
  `function_type_number` enum('Biological Process','Cellural Component','GO','Molecular Function','IDs') NOT NULL,
  PRIMARY KEY (`uniprot_entry`,`Function_ID`,`function_type_number`),
  KEY `fk_Protein__Function_function` (`Function_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `rRNAs`
--

CREATE TABLE IF NOT EXISTS `rRNAs` (
  `rRNA_id` int(11) NOT NULL AUTO_INCREMENT,
  `chr_genbank_id` varchar(50) DEFAULT NULL,
  `start_pos` int(11) DEFAULT NULL,
  `end_pos` int(11) DEFAULT NULL,
  `sequence` text NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `family` varchar(50) DEFAULT NULL,
  `sequenceid` int(11) DEFAULT NULL,
  PRIMARY KEY (`rRNA_id`),
  KEY `fk_rRNAs_sequence` (`sequenceid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `sequence`
--

CREATE TABLE IF NOT EXISTS `sequence` (
  `sequence_id` int(11) NOT NULL AUTO_INCREMENT,
  `Initial_label` varchar(255) NOT NULL,
  `sequence` text NOT NULL,
  `Mature` tinyint(1) NOT NULL,
  `pre-miRNA` tinyint(1) NOT NULL,
  `tRNA` tinyint(1) NOT NULL,
  `rRNA` tinyint(1) NOT NULL,
  `snoRNA` tinyint(1) NOT NULL,
  `tRFs` tinyint(1) NOT NULL,
  `pseudo-hairpins` tinyint(1) NOT NULL,
  `Random` tinyint(1) NOT NULL,
  `G+C` float NOT NULL,
  `A+U` float NOT NULL,
  `AA` float NOT NULL,
  `AC` float NOT NULL,
  `AG` float NOT NULL,
  `AU` float NOT NULL,
  `CA` float NOT NULL,
  `CC` float NOT NULL,
  `CG` float NOT NULL,
  `CU` float NOT NULL,
  `GA` float NOT NULL,
  `GC` float NOT NULL,
  `GG` float NOT NULL,
  `GU` float NOT NULL,
  `UA` float NOT NULL,
  `UC` float NOT NULL,
  `UG` float NOT NULL,
  `UU` float NOT NULL,
  `MFEI1` float NOT NULL,
  `MFEI2` float NOT NULL,
  `MFEI3` float NOT NULL,
  `MFEI4` float NOT NULL,
  `MFEI5` float NOT NULL,
  `dG` float NOT NULL,
  `dP` float NOT NULL,
  `dD` float NOT NULL,
  `dQ` float NOT NULL,
  `PosEntropy` float NOT NULL,
  `EAFE` float NOT NULL,
  `Div/ty` float NOT NULL,
  `Freq` float NOT NULL,
  `Diff` float NOT NULL,
  `dH` float NOT NULL,
  `dH/L` float NOT NULL,
  `dS` float NOT NULL,
  `dS/L` float NOT NULL,
  `Tm` float NOT NULL,
  `Tm/L` float NOT NULL,
  `|A-U|/L` float NOT NULL,
  `|G-C|/L` float NOT NULL,
  `|G-U|/L` float NOT NULL,
  `Avg_BP_stems` float NOT NULL,
  `(A-U)/stems` float NOT NULL,
  `(G-C)/stems` float NOT NULL,
  `(G-U)/stems` float NOT NULL,
  `G/C` float NOT NULL,
  `BP/GC` float NOT NULL,
  `BP/AU` float NOT NULL,
  `BP/GU` float NOT NULL,
  `Len` float NOT NULL,
  `CE/L` float NOT NULL,
  `CE_dist` float NOT NULL,
  `zG` float NOT NULL,
  `zP` float NOT NULL,
  `zD` float NOT NULL,
  `zQ` float NOT NULL,
  `zsP` float NOT NULL,
  `dF` float NOT NULL,
  PRIMARY KEY (`sequence_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `snoRNAs`
--

CREATE TABLE IF NOT EXISTS `snoRNAs` (
  `sno_id` int(11) NOT NULL AUTO_INCREMENT,
  `chr_genbank_id` varchar(50) DEFAULT NULL,
  `start_pos` int(11) DEFAULT NULL,
  `end_pos` int(11) DEFAULT NULL,
  `sequence` text NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `family` varchar(50) DEFAULT NULL,
  `sequenceid` int(11) DEFAULT NULL,
  PRIMARY KEY (`sno_id`),
  KEY `fk_snoRNAs_sequence` (`sequenceid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `tRFs`
--

CREATE TABLE IF NOT EXISTS `tRFs` (
  `tRF_id` int(11) NOT NULL AUTO_INCREMENT,
  `mintbase_ID` varchar(255) DEFAULT NULL,
  `trfdb_id` varchar(50) DEFAULT NULL,
  `chromosome` varchar(255) DEFAULT NULL,
  `start_pos_chr` int(11) DEFAULT NULL,
  `end_pos_chr` int(11) DEFAULT NULL,
  `start_pos_tRNA` int(11) DEFAULT NULL,
  `end_pos_tRNA` int(11) DEFAULT NULL,
  `sequence` varchar(50) NOT NULL,
  `tRF_type` varchar(7) DEFAULT NULL,
  `tRNAid` int(11) DEFAULT NULL,
  `sequenceid` int(11) DEFAULT NULL,
  PRIMARY KEY (`tRF_id`),
  KEY `fk_tRNAs_tRFs` (`tRNAid`),
  KEY `fk_tRFs_sequence` (`sequenceid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `tRNAs`
--

CREATE TABLE IF NOT EXISTS `tRNAs` (
  `tRNA_id` int(11) NOT NULL AUTO_INCREMENT,
  `chr_genbank_id` varchar(50) DEFAULT NULL,
  `start_pos` int(11) DEFAULT NULL,
  `end_pos` int(11) DEFAULT NULL,
  `sequence` text NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `family` varchar(50) DEFAULT NULL,
  `sequenceid` int(11) DEFAULT NULL,
  PRIMARY KEY (`tRNA_id`),
  KEY `fk_tRNAs_sequence` (`sequenceid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `miRNA_mature_Genes` (
  `mature_id` VARCHAR(50) NOT NULL,
  `gene_name` VARCHAR(50) NOT NULL,
  `score` FLOAT,
  PRIMARY KEY (`mature_id`, `gene_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Περιορισμοί για άχρηστους πίνακες
--

--
-- Περιορισμοί για πίνακα `Gene_Protein`
--
ALTER TABLE `Gene_Protein`
  ADD CONSTRAINT `fk_Gene_Protein__protein` FOREIGN KEY (`protein_uniprot_entry`) REFERENCES `Proteins` (`uniprot_entry`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_Gene_Protein_gene` FOREIGN KEY (`gene_stable_id`) REFERENCES `Genes` (`gene_stable_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `miRNAs_mature`
--
ALTER TABLE `miRNAs_mature`
  ADD CONSTRAINT `fk_mature_stem` FOREIGN KEY (`stemid`) REFERENCES `miRNAs_stem` (`miRNAstem_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_miRNAs_mature_sequence` FOREIGN KEY (`sequenceid`) REFERENCES `sequence` (`sequence_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `miRNAs_stem`
--
ALTER TABLE `miRNAs_stem`
  ADD CONSTRAINT `fk_miRNAs_stem_sequence` FOREIGN KEY (`sequenceid`) REFERENCES `sequence` (`sequence_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `Protein_Function`
--
ALTER TABLE `Protein_Function`
  ADD CONSTRAINT `fk_Protein_Function_protein` FOREIGN KEY (`uniprot_entry`) REFERENCES `Proteins` (`uniprot_entry`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_Protein__Function_function` FOREIGN KEY (`Function_ID`) REFERENCES `Function_descriptions` (`Function_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `rRNAs`
--
ALTER TABLE `rRNAs`
  ADD CONSTRAINT `fk_rRNAs_sequence` FOREIGN KEY (`sequenceid`) REFERENCES `sequence` (`sequence_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `snoRNAs`
--
ALTER TABLE `snoRNAs`
  ADD CONSTRAINT `fk_snoRNAs_sequence` FOREIGN KEY (`sequenceid`) REFERENCES `sequence` (`sequence_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `tRFs`
--
ALTER TABLE `tRFs`
  ADD CONSTRAINT `fk_tRFs_sequence` FOREIGN KEY (`sequenceid`) REFERENCES `sequence` (`sequence_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_tRNAs_tRFs` FOREIGN KEY (`tRNAid`) REFERENCES `tRNAs` (`tRNA_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `tRNAs`
--
ALTER TABLE `tRNAs`
  ADD CONSTRAINT `fk_tRNAs_sequence` FOREIGN KEY (`sequenceid`) REFERENCES `sequence` (`sequence_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
