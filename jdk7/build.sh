# build missing header files, "apt-file search missing-header-name" to get the package required
#export JAVA_HOME=/usr/lib/jvm/java-1.6.0-openjdk-amd64
export EXTRA_LIBS=/usr/lib/x86_64-linux-gnu/libasound.so.2 JAVA_BOOT_HOME=/usr/lib/jvm/java-1.6.0-openjdk-amd64 JAVA_IMPORT_HOME=/usr/lib/jvm/java-1.6.0-openjdk-amd64 ALT_BOOTDIR=/usr/lib/jvm/java-1.6.0-openjdk-amd64 ALT_JDK_IMPORT_PATH=/usr/lib/jvm/java-1.6.0-openjdk-amd64 ALLOW_DOWNLOADS=true  BUILD_NUMBER=b00  LANG=C  LD_LIBRARY_PATH=
#make clean 
make sanity all
