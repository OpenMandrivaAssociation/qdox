Name:           qdox
Version:        1.9.2
Release:        7
Epoch:          0
Summary:        Extract class/interface/method definitions from sources
License:        Apache License
URL:            http://qdox.codehaus.org/
Group:          Development/Java
Source0:        %{name}-%{version}.tar.bz2
#svn export http://svn.codehaus.org/qdox/tags/qdox-%{version}
#tar cvjf qdox-%{version}.tar.gz qdox-%{version}
Source1:        qdox-build.xml
Source2:        qdox-LocatedDef.java
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-junit >= 0:1.6
BuildRequires:  ant-nodeps >= 0:1.6
BuildRequires:  junit >= 0:3.8.1
BuildRequires:  java-cup
BuildRequires:  jflex
BuildRequires:  byaccj
Requires:       jpackage-utils
Requires:       java
BuildArch:      noarch
BuildRequires:  java-1.6.0-openjdk-devel

%description
QDox is a high speed, small footprint parser 
for extracting class/interface/method definitions 
from source files complete with JavaDoc @tags. 
It is designed to be used by active code 
generators or documentation tools. 

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
%{summary}.

%prep
%setup -q
cp %{SOURCE2} src/java/com/thoughtworks/qdox/parser/structs/LocatedDef.java 
cp %{SOURCE1} build.xml

#Remove files which needed jmock
rm src/test/com/thoughtworks/qdox/parser/MockBuilder.java
rm src/test/com/thoughtworks/qdox/parser/MockLexer.java
rm src/test/com/thoughtworks/qdox/parser/ParserTest.java
rm src/test/com/thoughtworks/qdox/directorywalker/DirectoryScannerTest.java

%{__perl} -pi -e 's/fork="yes"/fork="no"/g;' build.xml
%{__perl} -pi -e 's/yy_lexical_state/zzLexicalState/g;' src/grammar/lexer.flex

%build
export CLASSPATH=$(build-classpath \
ant \
ant-launcher \
java-cup \
jflex \
junit)
CLASSPATH=target/classes:target/test-classes:$CLASSPATH
%{ant} -Dbuild.sysclasspath=only jar javadoc

%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/%{name}.jar \
      $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; \
do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr build/javadocdir/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt README.txt
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/*
