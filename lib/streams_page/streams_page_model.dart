import '/flutter_flow/flutter_flow_util.dart';
import 'streams_page_widget.dart' show StreamsPageWidget;
import 'package:flutter/material.dart';

class StreamsPageModel extends FlutterFlowModel<StreamsPageWidget> {
  ///  State fields for stateful widgets in this page.

  final unfocusNode = FocusNode();

  /// Initialization and disposal methods.

  @override
  void initState(BuildContext context) {}

  @override
  void dispose() {
    unfocusNode.dispose();
  }

  /// Action blocks are added here.

  /// Additional helper methods are added here.
}
