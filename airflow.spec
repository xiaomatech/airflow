%global __os_install_post %{nil}

Name:           airflow
Version:        %{VERSION}
Release:        1%{?dist}
Summary:        Airflow
Group:			System Environment/Daemons       
License:        ASL 2.0
URL:            https://airflow.incubator.apache.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	python-devel
BuildRequires: 	mariadb-devel
BuildRequires:  libffi-devel 
BuildRequires:  cyrus-sasl-devel
BuildRequires:	gcc-c++
BuildRequires:	python2-pip
AutoReqProv: 	no
Requires:       python
Packager:       xianhua wei <xianhuawei.zhcn@gmail.com>

%description
Airflow is a platform to programmatically author, schedule and monitor workflows.

%install
%{__rm} -rf %{buildroot}

%{__mkdir} -p %{buildroot}/usr/share/airflow/bin/
%{__mkdir} -p %{buildroot}/usr/share/airflow/log/
%{__mkdir} -p %{buildroot}/etc/sysconfig/
%{__mkdir} -p %{buildroot}/etc/tmpfiles.d/
%{__mkdir} -p %{buildroot}/usr/lib/systemd/system/
%{__mkdir} -p %{buildroot}/usr/bin/
%{__mkdir} -p %{buildroot}/run/airflow/
%{__mkdir} -p %{buildroot}/etc/logrotate.d/

pip install --target %{buildroot}/usr/share/airflow/lib airflow[%{PACKAGES}]

%{__cp} -rp %{_topdir}/requirements.txt %{buildroot}/requirements.txt
pip install --target %{buildroot}/usr/share/airflow/lib -r %{buildroot}/requirements.txt
%{__cp} -rp %{_topdir}/systemd/airflow.cfg %{buildroot}/etc/airflow.cfg

%{__cp} -rp %{_topdir}/systemd/airflow %{buildroot}/etc/sysconfig/
%{__cp} -rp %{_topdir}/systemd/airflow.conf %{buildroot}/etc/tmpfiles.d/
%{__cp} -rp %{_topdir}/systemd/*.service %{buildroot}/usr/lib/systemd/system/
chmod 644 %{buildroot}/usr/lib/systemd/system/*

%{__cp} -rp %{_topdir}/bin/airflow %{buildroot}/usr/share/airflow/bin/
%{__cp} -rp %{_topdir}/bin/airflow.bash %{buildroot}/usr/bin/airflow

%{__cp} -rp %{_topdir}/bin/gunicorn %{buildroot}/usr/share/airflow/bin/
%{__cp} -rp %{_topdir}/bin/gunicorn.bash %{buildroot}/usr/bin/gunicorn

%{__cp} -rp %{_topdir}/logrotate/* %{buildroot}/etc/logrotate.d/

%pre
if ! /usr/bin/id airflow &>/dev/null; then
    /usr/sbin/useradd -r -d /usr/share/airflow -s /bin/sh -c "airflow" airflow|| \
        %logmsg "Unexpected error adding user \"airflow\". Aborting installation."
fi

%post
systemctl daemon-reload

%preun
systemctl stop airflow-flower
systemctl stop airflow-kerberos
systemctl stop airflow-scheduler
systemctl stop airflow-webserver
systemctl stop airflow-worker

%postun
systemctl daemon-reload
if [ $1 -eq 0 ]; then
	/usr/sbin/userdel airflow || %logmsg "User \"airflow\" could not be deleted."
fi

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,airflow,airflow,-)
/usr/share/airflow/
/run/airflow/

%defattr(-,root,root,-)
/etc/sysconfig/*
/etc/tmpfiles.d/*
/usr/lib/systemd/system/*
/usr/bin/*
/etc/logrotate.d/*
/etc/airflow.cfg

%changelog
