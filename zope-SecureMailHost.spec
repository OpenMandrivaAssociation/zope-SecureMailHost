%define Product SecureMailHost
%define product securemailhost
%define name    zope-%{Product}
%define version 1.1
%define release %mkrel 7

%define zope_minver     2.7
%define zope_home       %{_prefix}/lib/zope
%define software_home   %{zope_home}/lib/python

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:    Reimplementation of the standard MailHost
License:    ZPL
Group:      System/Servers
URL:        https://plone.org/products/%{product}
Source:     http://plone.org/products/%{product}/releases/%{version}/%{Product}-%{version}.tar.gz
Requires:   zope >= %{zope_minver}
BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}

%description
SecureMailHost is a reimplementation of the standard MailHost with some 
security and usability enhancements:

  * ESMTP login on the mail server based on the MailHost from
    http://www.zope.org/Members/bowerymarc

  * Start TLS (ssl) connection if possible

  * Usage of Python 2.3's email package which has multiple benefits like 
    easy to generate multi part messages including fance HTML emails and 
    with images.

  * REMOVED
    Releases are shipped with a compatibility version of email for older
    pythons.

  * A new secureSend() method that separates headers like mail to, mail from
    from the body text. You don't need to mingle body text and headers any 
    more.

  * Email address validation based on the code form PloneTool for mail from,
    mail to, carbon copy and blin carbon copy to prevent spam attacks.
    (Only for secureSend()!)

  * Message-Id and X-Mailer header generation to lower the spam hit points of
    Spam Assassin.

  * REMOVED
     An async mailer thread is using a new thread to send emails including a
    separate Mail class and a MailQueue with auto-backup on the file system.
    The separate mail thread will prevent Zope from blocking while connecting
    to the external SMTP server.
    (Disabled by default)

%prep
%setup -c -q

%build
# Not much, eh? :-)


%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}/%{software_home}/Products
%{__cp} -a * %{buildroot}%{software_home}/Products/


%clean
%{__rm} -rf %{buildroot}

%post
if [ "`%{_prefix}/bin/zopectl status`" != "daemon manager not running" ] ; then
         service zope restart
fi

%postun
if [ -f "%{_prefix}/bin/zopectl" ] && [ "`%{_prefix}/bin/zopectl status`" != "daemon manager not running" ] ; then
         service zope restart
fi

%files
%defattr(-,root,root)
%{software_home}/Products/*
