#
# PySNMP MIB module VMWARE-PRODUCTS-MIB (http://pysnmp.sf.net)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/VMWARE-PRODUCTS-MIB
# Produced by pysmi-0.2.2 at Thu Apr 05 18:52:46 2018
# On host ? platform ? version ? by user ?
# Using Python version 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:25:58) [MSC v.1500 64 bit (AMD64)]
#
Integer, ObjectIdentifier, OctetString = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
NamedValues, = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
ConstraintsUnion, SingleValueConstraint, ConstraintsIntersection, ValueSizeConstraint, ValueRangeConstraint = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsUnion", "SingleValueConstraint", "ConstraintsIntersection", "ValueSizeConstraint", "ValueRangeConstraint")
NotificationGroup, ModuleCompliance = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance")
Integer32, MibScalar, MibTable, MibTableRow, MibTableColumn, NotificationType, MibIdentifier, IpAddress, TimeTicks, Counter64, Unsigned32, iso, Gauge32, ModuleIdentity, ObjectIdentity, Bits, Counter32 = mibBuilder.importSymbols("SNMPv2-SMI", "Integer32", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "NotificationType", "MibIdentifier", "IpAddress", "TimeTicks", "Counter64", "Unsigned32", "iso", "Gauge32", "ModuleIdentity", "ObjectIdentity", "Bits", "Counter32")
DisplayString, TextualConvention = mibBuilder.importSymbols("SNMPv2-TC", "DisplayString", "TextualConvention")
vmwProductSpecific, vmwOID = mibBuilder.importSymbols("VMWARE-ROOT-MIB", "vmwProductSpecific", "vmwOID")
vmwProducts = ModuleIdentity((1, 3, 6, 1, 4, 1, 6876, 4, 11))
vmwProducts.setRevisions(('2014-09-19 00:00', '2011-09-29 00:00', '2007-07-30 00:00',))
if mibBuilder.loadTexts: vmwProducts.setLastUpdated('201409190000Z')
if mibBuilder.loadTexts: vmwProducts.setOrganization('VMware, Inc')
vmwESX = MibIdentifier((1, 3, 6, 1, 4, 1, 6876, 4, 1))
vmwDVS = MibIdentifier((1, 3, 6, 1, 4, 1, 6876, 4, 2))
vmwVC = MibIdentifier((1, 3, 6, 1, 4, 1, 6876, 4, 3))
vmwServer = MibIdentifier((1, 3, 6, 1, 4, 1, 6876, 4, 4))
vmwVCOps = MibIdentifier((1, 3, 6, 1, 4, 1, 6876, 4, 5))
vmwGenericAppliance = MibIdentifier((1, 3, 6, 1, 4, 1, 6876, 4, 6))
vmwEmbeddedVirtualCenterAppliance = MibIdentifier((1, 3, 6, 1, 4, 1, 6876, 4, 7))
vmwInfrastructureAppliance = MibIdentifier((1, 3, 6, 1, 4, 1, 6876, 4, 8))
vmwManagementAppliance = MibIdentifier((1, 3, 6, 1, 4, 1, 6876, 4, 9))
oidESX = MibIdentifier((1, 3, 6, 1, 4, 1, 6876, 60, 1))
mibBuilder.exportSymbols("VMWARE-PRODUCTS-MIB", vmwGenericAppliance=vmwGenericAppliance, vmwVCOps=vmwVCOps, vmwESX=vmwESX, vmwEmbeddedVirtualCenterAppliance=vmwEmbeddedVirtualCenterAppliance, vmwManagementAppliance=vmwManagementAppliance, vmwServer=vmwServer, oidESX=oidESX, PYSNMP_MODULE_ID=vmwProducts, vmwDVS=vmwDVS, vmwVC=vmwVC, vmwInfrastructureAppliance=vmwInfrastructureAppliance, vmwProducts=vmwProducts)
