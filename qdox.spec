Summary:	Extract class/interface/method definitions from sources
Name:		qdox
Version:	1.12.1
Release:	2
License:	Apache License
Group:		Development/Java
Url:		http://qdox.codehaus.org/
Source0:	http://repo.maven.apache.org/maven2/com/thoughtworks/qdox/qdox/%{version}/qdox-%{version}-sources.jar
#svn export http://svn.codehaus.org/qdox/tags/qdox-%{version}
#tar cvjf qdox-%{version}.tar.gz qdox-%{version}
BuildArch:	noarch
BuildRequires:	ant >= 0:1.6
BuildRequires:	ant-junit >= 0:1.6
BuildRequires:	ant-nodeps >= 0:1.6
BuildRequires:	byaccj
BuildRequires:	java-cup
BuildRequires:	java-rpmbuild >= 0:1.6
BuildRequires:	jflex
BuildRequires:	java-1.6.0-openjdk-devel
BuildRequires:	junit >= 0:3.8.1
Requires:	jpackage-utils
Requires:	java

%track
prog %{name} = {
	url = http://qdox.codehaus.org/download.html
	regex = "Latest stable release - QDox (__VER__):"
	version = %{version}
}

%description
QDox is a high speed, small footprint parser 
for extracting class/interface/method definitions 
from source files complete with JavaDoc @tags. 
It is designed to be used by active code 
generators or documentation tools. 

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description javadoc
%{summary}.

%prep
%setup -qc %{name}-%{version}

%build
find . -name "*.java" |xargs javac -classpath $(build-classpath junit ant)
find . -name "*.class" |xargs jar cf %{name}-%{version}.jar META-INF
find . -name "*.java" |xargs javadoc -d apidocs

%install
# jars
mkdir -p %{buildroot}%{_javadir}
cp -p %{name}-%{version}.jar %{buildroot}%{_javadir}/
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; \
do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr apidocs/* %{buildroot}%{_javadocdir}/%{name}

%files
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar

%files javadoc
%doc %{_javadocdir}/*

