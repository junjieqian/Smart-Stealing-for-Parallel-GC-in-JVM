#!/bin/bash

if [ ! -d "/opt/various_APP" ]; then
  mkdir /opt/various_APP
fi
LOGFILE=/opt/various_APP/

DefaultJava=/opt/baseline_default/jdk7/build/linux-amd64/bin/java
NoStealing=/opt/baseline_nostealing/jdk7/build/linux-amd64/bin/java
SmartStealing=/home/jqian/src/cost-aware-parallel-garbage-collection/jdk7/build/linux-amd64/bin/java

Dacapo=/home/jqian/benchmarks/dacapo-9.12-bach.jar
declare -A dacapobenchmark
dacapobenchmark=(["eclipse"]="330m" ["jython"]="90m" ["lusearch"]="90m" ["pmd"]="210m" ["sunflow"]="210m" ["avrora"]="75m" ["xalan"]="150m" ["h2"]="900m" ["tomcat"]="135m")

SPECJVM=/home/jqian/benchmarks/SPECjvm2008/SPECjvm2008.jar
declare -A specbenchmark
specbenchmark=(["compiler.sunflow"]="8000m" ["crypto.aes"]="4000m" ["scimark.fft.large"]="6000m" ["xml.validation"]="4000m" ["xml.transform"]="4000m")

for thread in {1..128..4}; do
  for i in {1..3}; do
    for name in "${!dacapobenchmark[@]}"; do
      echo "$name-${dacapobenchmark["$name"]}-$thread-$i"
      $DefaultJava -Xms${dacapobenchmark["$name"]} -Xmx${dacapobenchmark["$name"]} -verbose:gc -XX:+PrintGCDetails -jar $Dacapo $name -t $thread -s large &>> $LOGFILE"$name"_"$thread"_"default"

      $NoStealing -Xms${dacapobenchmark["$name"]} -Xmx${dacapobenchmark["$name"]} -verbose:gc -XX:+PrintGCDetails -jar $Dacapo $name -t $thread -s large &>> $LOGFILE"$name"_"$thread"_"nostealing"

      $SmartStealing -Xms${dacapobenchmark["$name"]} -Xmx${dacapobenchmark["$name"]} -verbose:gc -XX:+PrintGCDetails -jar $Dacapo $name -t $thread -s large &>> $LOGFILE"$name"_"$thread"_"smartstealing"
    done
  done
done

cd /home/jqian/benchmarks/SPECjvm2008
for thread in {1..128..4}; do
  for i in {1..3}; do
    for name in "xml.validation" "xml.transform"; do
      echo "$name-${specbenchmark["$name"]}-$thread-$i"
      /opt/baseline_default/jdk7/build/linux-amd64/j2sdk-image/jre/bin/java -Xbootclasspath/p:/opt/baseline_default/jdk7/build/linux-amd64/j2sdk-image/jre/lib/rt.jar -Xms${specbenchmark["$name"]} -Xmx${specbenchmark["$name"]} -verbose:gc -XX:+PrintGCDetails -jar $SPECJVM $name -bt $thread -ops 100 &>> $LOGFILE"$name"_"$thread"_"default"

      /opt/baseline_nostealing/jdk7/build/linux-amd64/j2sdk-image/jre/bin/java -Xbootclasspath/p:/opt/baseline_nostealing/jdk7/build/linux-amd64/j2sdk-image/jre/lib/rt.jar -Xms${specbenchmark["$name"]} -Xmx${specbenchmark["$name"]} -verbose:gc -XX:+PrintGCDetails -jar $SPECJVM $name -bt $thread -ops 100 &>> $LOGFILE"$name"_"$thread"_"nostealing"

      /home/jqian/src/cost-aware-parallel-garbage-collection/jdk7/build/linux-amd64/j2sdk-image/jre/bin/java -Xbootclasspath/p:/home/jqian/src/cost-aware-parallel-garbage-collection/jdk7/build/linux-amd64/j2sdk-image/jre/lib/rt.jar -Xms${specbenchmark["$name"]} -Xmx${specbenchmark["$name"]} -verbose:gc -XX:+PrintGCDetails -jar $SPECJVM $name -bt $thread -ops 100 &>> $LOGFILE"$name"_"$thread"_"smartstealing"
    done
  done
done
