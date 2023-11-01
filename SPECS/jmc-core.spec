# Version
%global major 7
%global minor 1
%global patchlevel 1

# Revision
%global revnum 5
# set to 1 for hg snapshots, 0 for release
%global usesnapshot 0

# SNAPSHOT version
%global hgrevhash 63ec7d0ee8d9
%global hgrevdate 20200608

%global tarball_name jmc7-%{hgrevhash}

%if %{usesnapshot}
  %global releasestr %{revnum}.%{hgrevdate}hg%{hgrevhash}
%else
  %global releasestr %{revnum}
%endif

Name:     jmc-core
Version:  %{major}.%{minor}.%{patchlevel}
Release:  %{releasestr}%{?dist}.2
Summary:  Core API for JDK Mission Control
# jmc source README.md states: The Mission Control source code is made
# available under the Universal Permissive License (UPL), Version 1.0 or a
# BSD-style license, alternatively. The full open source license text is
# available at license/LICENSE.txt in the JMC project.
License:  UPL or BSD
URL:      http://openjdk.java.net/projects/jmc/

Source0:    https://hg.openjdk.java.net/jmc/jmc7/archive/%{hgrevhash}.tar.gz

BuildArch:  noarch

BuildRequires:  maven-local
BuildRequires:  mvn(org.owasp.encoder:encoder)

# maven requires generator will add Require for runtime dependency
#   on mvn(org.owasp.encoder:encoder)

%description
JDK Mission Control is an advanced set of tools that enables efficient and
detailed analysis of the extensive data collected by Flight Recorder. The
tool chain enables developers and administrators to collect and analyze data
from Java applications running locally or deployed in production environments.

%package javadoc
Summary:  Javadoc for %{name}

%description javadoc
%{summary}.

%prep
%setup -q -n %{tarball_name}/core
cp ../license/* ./
cp ../README.md ./

%pom_remove_plugin :nexus-staging-maven-plugin
%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :maven-javadoc-plugin

%pom_remove_plugin :jacoco-maven-plugin tests
%pom_disable_module coverage

# don't install test packages
%mvn_package org.openjdk.jmc:missioncontrol.core.tests __noinstall
%mvn_package org.openjdk.jmc:flightrecorder.test __noinstall
%mvn_package org.openjdk.jmc:flightrecorder.rules.test __noinstall
%mvn_package org.openjdk.jmc:flightrecorder.rules.jdk.test __noinstall

%build
# some tests require large heap and fail with OOM
# depending on the builder resources
%mvn_build -- -Dmaven.test.failure.ignore=true

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt
%license THIRDPARTYREADME.txt
%doc README.md

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt
%license THIRDPARTYREADME.txt
%doc README.md

%changelog
* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 7.1.1-5.2
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Sep 21 2020 Jie Kang <jkang@redhat.com> - 7.1.1-5
- Update license
* Fri Aug 28 2020 Jie Kang <jkang@redhat.com> - 7.1.1-4
- Update to latest upstream 63ec7d0ee8d9
* Mon Apr 27 2020 Jie Kang <jkang@redhat.com> - 7.1.1-3
- Update to upstream 7.1.1 ga commit
* Wed Mar 11 2020 Alex Macdonald <almacdon@redhat.com> - 7.1.1-2
- Update to latest upstream to include JMC-6728
* Fri Feb 28 2020 Alex Macdonald <almacdon@redhat.com> - 7.1.1-1
- Update to latest upstream
* Fri Dec 20 2019 Alex Macdonald <almacdon@redhat.com> - 7.1.0-1
- Update to latest upstream (7.1.0-ga) and disable jacoco & coverage
* Tue Sep 24 2019 Jie Kang <jkang@redhat.com> - 7.0.0-2
- Update to latest upstream with minor bug fixes
* Thu Aug 15 2019 Jie Kang <jkang@redhat.com> - 7.0.0-1
- Exclude test packages
* Fri May 31 2019 Jie Kang <jkang@redhat.com> - 7.0.0-0
- Initial package
