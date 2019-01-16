#!/bin/csh -f
#  run_all_precincts.sh.cmd
#
#  UGE job for run_all_precincts.sh built Mon Jul 24 16:40:21 PDT 2017
#
#  The following items pertain to this script
#  Use current working directory
#$ -cwd
#  input           = /dev/null
#  output          = /u/home/m/mhfeng/scripts/run_all_precincts.sh.joblog.$JOB_ID
#$ -o /u/home/m/mhfeng/scripts/run_all_precincts.sh.joblog.$JOB_ID
#  error           = Merged with joblog
#$ -j y
#  The following items pertain to the user program
#  user program    = /u/home/m/mhfeng/scripts/run_all_precincts.sh
#  arguments       = 
#  program input   = Specified by user program
#  program output  = Specified by user program
#  Resources requested
#
#$ -l h_data=4096M,h_rt=8:00:00
# #
#  Name of application for log
#$ -v QQAPP=job
#  Email address to notify
#$ -M mhfeng@mail
#  Notify at beginning and end of job
#$ -m bea
#  Job is not rerunable
#$ -r n
#
# Initialization for serial execution
#
  unalias *
  set qqversion = 
  set qqapp     = "job serial"
  set qqidir    = /u/home/m/mhfeng/scripts
  set qqjob     = run_all_precincts.sh
  set qqodir    = /u/home/m/mhfeng/scripts
  cd     /u/home/m/mhfeng/scripts
  source /u/local/bin/qq.sge/qr.runtime
  if ($status != 0) exit (1)
#
  echo "UGE job for run_all_precincts.sh built Mon Jul 24 16:40:21 PDT 2017"
  echo ""
  echo "  run_all_precincts.sh directory:"
  echo "    "/u/home/m/mhfeng/scripts
  echo "  Submitted to UGE:"
  echo "    "$qqsubmit
  echo "  SCRATCH directory:"
  echo "    "$qqscratch
#
  echo ""
  echo "run_all_precincts.sh started on:   "` hostname -s `
  echo "run_all_precincts.sh started at:   "` date `
  echo ""
#
# Run the user program
#
  source /u/local/Modules/default/init/modules.csh
  module load intel/13.cs
#
  echo run_all_precincts.sh "" \>\& run_all_precincts.sh.output.$JOB_ID
  echo ""
  time /u/home/m/mhfeng/scripts/run_all_precincts.sh  >& /u/home/m/mhfeng/scripts/run_all_precincts.sh.output.$JOB_ID
#
  echo ""
  echo "run_all_precincts.sh finished at:  "` date `
#
# Cleanup after serial execution
#
  source /u/local/bin/qq.sge/qr.runtime
#
  echo "-------- /u/home/m/mhfeng/scripts/run_all_precincts.sh.joblog.$JOB_ID --------" >> /u/local/apps/queue.logs/job.log.serial
  if (`wc -l /u/home/m/mhfeng/scripts/run_all_precincts.sh.joblog.$JOB_ID  | awk '{print $1}'` >= 1000) then
	head -50 /u/home/m/mhfeng/scripts/run_all_precincts.sh.joblog.$JOB_ID >> /u/local/apps/queue.logs/job.log.serial
	echo " "  >> /u/local/apps/queue.logs/job.log.serial
	tail -10 /u/home/m/mhfeng/scripts/run_all_precincts.sh.joblog.$JOB_ID >> /u/local/apps/queue.logs/job.log.serial
  else
	cat /u/home/m/mhfeng/scripts/run_all_precincts.sh.joblog.$JOB_ID >> /u/local/apps/queue.logs/job.log.serial
  endif
  exit (0)
