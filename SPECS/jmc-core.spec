# Version
%global major 8
%global minor 0
%global patchlevel 1

# Revision
%global revnum 2
# set to 1 for snapshots, 0 for release
%global usesnapshot 0

# SNAPSHOT version
%global revhash 699a121bd449fe8a9350221282bd3f809691a766
%global revdate 20210623

%global tarball_name jmc-%{revhash}

%if %{usesnapshot}
  %global releasestr %{revnum}.%{revdate}
%else
  %global releasestr %{revnum}
%endif


# Don't require junit
%global __requires_exclude ^osgi\\(org.junit.*$

Name:     jmc-core
Version:  %{major}.%{minor}.%{patchlevel}
Release:  %{releasestr}%{?dist}
Summary:  Core API for JDK Mission Control

License:  UPL
URL:      http://openjdk.java.net/projects/jmc/

Source0:    https://github.com/openjdk/jmc/archive/%{revhash}.tar.gz

BuildArch:  noarch
ExclusiveArch: x86_64

# Change common manifest to reference lz4-java
Patch0:    0-amend-lz4-java-reference.patch

BuildRequires:  maven-local
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.commonjava.maven.plugins:directory-maven-plugin)
BuildRequires:  mvn(org.owasp.encoder:encoder)

BuildRequires: lz4-java

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

%patch0 -p1

%pom_remove_plugin :nexus-staging-maven-plugin
%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :jacoco-maven-plugin tests

%pom_disable_module coverage
%pom_disable_module org.openjdk.jmc.flightrecorder.writer

# don't install test packages (aside from flightrecorder.test)
%mvn_package org.openjdk.jmc:missioncontrol.core.tests __noinstall
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
* Tue Oct 05 2021 Alex Macdonald <almacdon@redhat.com> - 8.0.1-2
- Rebuild with updated dependencies

* Tue Aug 17 2021 Alex Macdonald <almacdon@redhat.com> - 8.0.1-1
- Revert jmc packages to 8.0.1 release

* Tue Aug 10 2021 Alex Macdonald <almacdon@redhat.com> - 8.1.0-1
- Update to jmc-ga tagged commit d0f89f0

* Fri Feb 12 2021 Alex Macdonald <almacdon@redhat.com> - 8.0.0-1
- Update to jmc8 branch commit 8ab40bf

* Thu Apr 23 2020 Alex Macdonald <almacdon@redhat.com> - 7.1.1-3
- Update to latest commit e67446b5fc9d

* Fri Apr 17 2020 Alex Macdonald <almacdon@redhat.com> - 7.1.1-2
- remove plugins from pom (maven-source-plugin, jacoco)

* Thu Apr 16 2020 Alex Macdonald <almacdon@redhat.com> - 7.1.1-1
- Updated to version 7.1.1

* Thu Nov 14 2019 Jie Kang <jkang@redhat.com> - 7.0.0-3
- Don't require junit

* Wed Nov 13 2019 Jie Kang <jkang@redhat.com> - 7.0.0-2
- Exclude test packages

* Tue Mar 12 2019 Jie Kang <jkang@redhat.com> - 7.0.0-1
- Initial package
