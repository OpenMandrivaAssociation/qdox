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

%define gcj_support 0

Name:           qdox
Version:        1.9.2
Release:        %mkrel 5
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
%if %{gcj_support}
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


%changelog
* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.9.2-4mdv2011.0
+ Revision: 607261
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.9.2-2mdv2010.1
+ Revision: 523882
- rebuilt for 2010.1

* Mon Jul 13 2009 Frederik Himpe <fhimpe@mandriva.org> 0:1.9.2-1mdv2010.0
+ Revision: 395695
- Update to new version 1.9.2
- Build with default Java SDK (rpmbuild-java) instead of gcj

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0:1.6.3-1.1.5mdv2009.1
+ Revision: 351584
- rebuild

* Wed Mar 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0:1.6.3-1.1.4mdv2008.1
+ Revision: 179397
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.6.3-1.1.2mdv2008.0
+ Revision: 87347
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Mon Jul 09 2007 David Walluck <walluck@mandriva.org> 0:1.6.3-1.1.1mdv2008.0
+ Revision: 50715
- 1.6.3

* Wed Jul 04 2007 David Walluck <walluck@mandriva.org> 0:1.5-2.1.1mdv2008.0
+ Revision: 48002
- Import qdox



* Thu Feb 15 2007 Permaine Cheung <pcheung@redhat.com> - 0:1.5-2jpp.1
- Use ant for building, and fixes as per fedora guidelines.

* Mon Feb 20 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.5-2jpp
- Rebuild for JPP-1.7, adapting to maven-1.1

* Wed Nov 16 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.5-1jpp
- Upgrade to 1.5
- Build is now done with maven and requires jflex and byaccj

* Wed Aug 25 2004 Fernando Nasser <fnasser@redhat.com> - 0:1.4-3jpp
- Rebuild with Ant 1.6.2

* Fri Aug 06 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.4-2jpp
- Upgrade to ant-1.6.X

* Mon Jun 07 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.4-1jpp
- Upgrade to 1.4
- Drop Requires: mockobjects (Build/Test only)

* Tue Feb 24 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.3-1jpp
- First JPackage release
