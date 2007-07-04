# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support 1

Name:           qdox
Version:        1.5
Release:        %mkrel 2.1.1
Epoch:          0
Summary:        Extract class/interface/method definitions from sources
License:        Apache License
URL:            http://qdox.codehaus.org/
Group:          Development/Java
Source0:        qdox-1.5-src.tar.gz
#svn export http://svn.codehaus.org/qdox/tags/QDOX_1_5/qdox/
#tar czvf qdox-1.5-src.tar.gz qdox
Source1:        qdox-build.xml
Source2:        qdox-LocatedDef.java
Patch0:         qdox-1.5-parser_y.patch
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-junit >= 0:1.6
BuildRequires:  ant-nodeps >= 0:1.6
BuildRequires:  junit >= 0:3.8.1
BuildRequires:  java-cup
BuildRequires:  jflex
BuildRequires:  byaccj
Requires:       jpackage-utils
Requires:       java
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

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
%setup -q -n %{name}
cp %{SOURCE2} src/java/com/thoughtworks/qdox/parser/structs/LocatedDef.java 
cp %{SOURCE1} build.xml

%patch0 -b .sav
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

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt README.txt
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/*
