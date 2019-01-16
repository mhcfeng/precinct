#!/bin/csh -f
#  run_one_precinct.cmd
#
#  UGE job for run_one_precinct built Wed Jul 26 09:44:24 PDT 2017
#
#  The following items pertain to this script
#  Use current working directory
#$ -cwd
#  input           = /dev/null
#  output          = /u/home/m/mhfeng/scripts/run_one_precinct.joblog.$JOB_ID
#$ -o /u/home/m/mhfeng/scripts/run_one_precinct.joblog.$JOB_ID
#  error           = Merged with joblog
#$ -j y
#  The following items pertain to the user program
#  user program    = /u/home/m/mhfeng/scripts/run_one_precinct.m
#  arguments       = 
#  program input   = Specified by user program
#  program output  = Specified by user program
#  Resources requested
#
#$ -l h_data=8192M,h_vmem=INFINITY,h_rt=8:00:00
# #
#  Name of application for log
#$ -v QQAPP=matlab
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
  set qqapp     = "matlab serial"
  set qqmtasks  = 1
  set qqidir    = /u/home/m/mhfeng/scripts
  set qqjob     = run_one_precinct
  set qqodir    = /u/home/m/mhfeng/scripts
  cd     /u/home/m/mhfeng/scripts
  source /u/local/bin/qq.sge/qr.runtime
  if ($status != 0) exit (1)
#
  echo "UGE job for run_one_precinct built Wed Jul 26 09:44:24 PDT 2017"
  echo ""
  echo "  run_one_precinct directory:"
  echo "    "/u/home/m/mhfeng/scripts
  echo "  Submitted to UGE:"
  echo "    "$qqsubmit
  echo "  SCRATCH directory:"
  echo "    "$qqscratch
#
  echo ""
  echo "run_one_precinct started on:   "` hostname -s `
  echo "run_one_precinct started at:   "` date `
  echo ""
#
# Run the user program
#
  source /u/local/Modules/default/init/modules.csh
  module load matlab
  setenv LM_LICENSE_FILE /u/local/licenses/license.matlab
  set path = ( $path /sbin )
#
  echo "mcc -m -R -nodisplay,-singleCompThread run_one_precinct.m"
requeue:
  /u/local/apps/matlab/8.6/bin/mcc -m -R -nodisplay,-singleCompThread run_one_precinct.m
  set rc = $status
  # waiting for bluearc per ppk
  sleep 60
  #
  if( `grep -c 'Maximum number of users'                  /u/home/m/mhfeng/scripts/run_one_precinct.joblog.$JOB_ID` > 0 ||\
      `grep -c 'Licensed number of users already reached' /u/home/m/mhfeng/scripts/run_one_precinct.joblog.$JOB_ID` > 0 ||\
      `grep -c 'License checkout failed'                  /u/home/m/mhfeng/scripts/run_one_precinct.joblog.$JOB_ID` > 0 ||\
      `grep -c 'Could not check out a Compiler license'   /u/home/m/mhfeng/scripts/run_one_precinct.joblog.$JOB_ID` > 0 ) then
    head -n 13 /u/home/m/mhfeng/scripts/run_one_precinct.joblog.$JOB_ID > /u/home/m/mhfeng/scripts/.$$
    mv /u/home/m/mhfeng/scripts/.$$ /u/home/m/mhfeng/scripts/run_one_precinct.joblog.$JOB_ID
    echo "------------ waiting for a license. retrying mcc command."
    sleep 90
    goto requeue
  endif # waiting for license
#
  echo ""
  if( $rc != 0 || ! -e /u/home/m/mhfeng/scripts/run_one_precinct ) then
    echo "============================================================"
    echo "matlab.queue mcc step failed with status $rc"
    echo "============================================================"
    #
    echo ============================================================ >> /u/home/m/mhfeng/scripts/run_one_precinct.output.$JOB_ID
    echo matlab.queue mcc step failed with status $rc >> /u/home/m/mhfeng/scripts/run_one_precinct.output.$JOB_ID
    echo ============================================================ >> /u/home/m/mhfeng/scripts/run_one_precinct.output.$JOB_ID
    # stop here if mcc failed
  else
    # execute mcc-compiled executable
    chmod +x /u/home/m/mhfeng/scripts/run_one_precinct
    echo run_one_precinct  \>\& run_one_precinct.output.$JOB_ID
    /usr/bin/time /u/home/m/mhfeng/scripts/run_one_precinct  >& /u/home/m/mhfeng/scripts/run_one_precinct.output.$JOB_ID
    set rc = $status
    #
    if( $rc != 0 ) then
      rm -f /u/home/m/mhfeng/scripts/run_one_precinct
      echo "matlab.queue execute mcc-compiled run_one_precinct step failed with status $rc"
      echo "retrying with matlab executable..."
      #
      echo matlab.queue execute mcc-compiled run_one_precinct step failed with status $rc >> /u/home/m/mhfeng/scripts/run_one_precinct.output.$JOB_ID
      echo retrying with matlab executable... >> /u/home/m/mhfeng/scripts/run_one_precinct.output.$JOB_ID
      #
      set qqargs = ( -nojvm -nodisplay -nosplash  )
      if( 1 == 1 ) set qqargs = ( -singleCompThread $qqargs )
      #
      # run with matlab
      echo matlab $qqargs -r run_one_precinct -logfile /u/home/m/mhfeng/scripts/run_one_precinct.output.$JOB_ID
requeue2:
      /usr/bin/time /u/local/apps/matlab/8.6/bin/matlab $qqargs -r run_one_precinct -logfile /u/home/m/mhfeng/scripts/run_one_precinct.output.$JOB_ID
      #
      # waiting for bluearc per ppk
      sleep 60
      #
      if( `grep -c 'Maximum number of users'                  /u/home/m/mhfeng/scripts/run_one_precinct.joblog.$JOB_ID` > 0 ||\
          `grep -c 'Licensed number of users already reached' /u/home/m/mhfeng/scripts/run_one_precinct.joblog.$JOB_ID` > 0 ||\
          `grep -c 'License checkout failed'                  /u/home/m/mhfeng/scripts/run_one_precinct.joblog.$JOB_ID` > 0 ) then
        head -n 17 /u/home/m/mhfeng/scripts/run_one_precinct.joblog.$JOB_ID > /u/home/m/mhfeng/scripts/.$$
        mv /u/home/m/mhfeng/scripts/.$$ /u/home/m/mhfeng/scripts/run_one_precinct.joblog.$JOB_ID
        echo "------------ waiting for a license. retrying matlab executable."
        sleep 90
        goto requeue2
      endif # waiting for license
    endif # execute mcc-executable failed
  endif # mcc step succeeded
#
  echo ""
  echo "run_one_precinct finished at:  "` date `
#
# Cleanup after serial execution
#
  rm -f /u/home/m/mhfeng/scripts/run_one_precinct.prj
  rm -f /u/home/m/mhfeng/scripts/run_one_precinct_main.c
  rm -f /u/home/m/mhfeng/scripts/run_one_precinct_mcc_component_data.c
  rm -f /u/home/m/mhfeng/scripts/mccExcludedFiles.log
  rm -f /u/home/m/mhfeng/scripts/readme.txt
  rm -f /u/home/m/mhfeng/scripts/run_run_one_precinct.sh

  source /u/local/bin/qq.sge/qr.runtime
#
  echo "-------- /u/home/m/mhfeng/scripts/run_one_precinct.joblog.$JOB_ID --------" >> /u/local/apps/queue.logs/matlab.log.serial
 if (`wc -l /u/home/m/mhfeng/scripts/run_one_precinct.joblog.$JOB_ID  | awk '{print $1}'` >= 1000) then
        head -50 /u/home/m/mhfeng/scripts/run_one_precinct.joblog.$JOB_ID >> /u/local/apps/queue.logs/matlab.log.serial
        echo " "  >> /u/local/apps/queue.logs/matlab.log.serial
        tail -10 /u/home/m/mhfeng/scripts/run_one_precinct.joblog.$JOB_ID >> /u/local/apps/queue.logs/matlab.log.serial
  else
        cat /u/home/m/mhfeng/scripts/run_one_precinct.joblog.$JOB_ID >> /u/local/apps/queue.logs/matlab.log.serial
  endif
  exit (0)
